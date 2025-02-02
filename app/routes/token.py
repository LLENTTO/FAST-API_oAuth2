"""
THIS IS THE TOKEN ENDPOINT
Handles OAuth callback, generates JWT, and saves user in MongoDB
"""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import jwt
from datetime import datetime, timedelta
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE
from app.oauth import oauth
from app.database import db
from app.models import Token

# Create Router
router = APIRouter()

def create_jwt_token(data: dict, expires_delta: timedelta = None):
    """
    Creates a JSON Web Token (JWT) with an expiration time.
    """
    to_encode = data.copy()
    now = datetime.utcnow()
    expire = now + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE))
    to_encode["exp"] = int(expire.timestamp())  # Convert datetime to Unix timestamp
    to_encode["iat"] = int(now.timestamp())       # Issued at claim
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.get("/token/{provider}", name="token_callback")
async def token_callback(request: Request, provider: str):
    """
    OAuth2 callback endpoint.
    After successful login, the provider redirects here.
    """
    # Only GitHub is supported for now.
    supported_providers = ["github"]
    if provider not in supported_providers:
        raise HTTPException(status_code=400, detail="Unsupported provider (Bad Request)")

    client = oauth.create_client(provider)
    if not client:
        raise HTTPException(
            status_code=400,
            detail=f"OAuth provider '{provider}' is not configured correctly."
        )

    # Ensure user was successfully authorized.
    try:
        token = await client.authorize_access_token(request)
    except Exception as e:  # Replace with more specific exceptions if available.
        raise HTTPException(status_code=400, detail=f"OAuth authorization failed: {str(e)}")

    # Retrieve user information from GitHub.
    user_info = None
    if provider == "github":
        try:
            res = await client.get("user", token=token)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error fetching user info: {str(e)}")

        # Check for a successful response.
        if hasattr(res, "status_code") and res.status_code != 200:
            raise HTTPException(
                status_code=res.status_code,
                detail="Failed to retrieve user info from GitHub"
            )
        user_info = res.json()

        # Fetch email if missing.
        if not user_info.get("email"):
            try:
                emails_resp = await client.get("user/emails", token=token)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error fetching user emails: {str(e)}")
            if hasattr(emails_resp, "status_code") and emails_resp.status_code != 200:
                raise HTTPException(
                    status_code=emails_resp.status_code,
                    detail="Failed to retrieve user emails from GitHub"
                )
            emails = emails_resp.json()
            primary_emails = [email for email in emails if email.get("primary") and email.get("verified")]
            if primary_emails:
                user_info["email"] = primary_emails[0]["email"]
            elif emails and emails[0].get("email"):
                user_info["email"] = emails[0]["email"]

    # If email is missing, raise an error.
    if not user_info or not user_info.get("email"):
        raise HTTPException(status_code=400, detail="Failed to retrieve user email from GitHub.")

    # Prepare user data with a fallback for full_name.
    user_data = {
        "email": user_info.get("email"),
        "full_name": user_info.get("name") or user_info.get("login") or user_info.get("email"),
        "provider": provider
    }

    # Save or update user in the database.
    users_collection = db.get_collection("users")
    existing_user = await users_collection.find_one({"email": user_data["email"]})
    if existing_user:
        user_id = str(existing_user["_id"])
        # Optionally update the user's full name if it has changed.
        if user_data["full_name"] != existing_user.get("full_name"):
            await users_collection.update_one(
                {"_id": existing_user["_id"]},
                {"$set": {"full_name": user_data["full_name"]}}
            )
    else:
        result = await users_collection.insert_one(user_data)
        user_id = str(result.inserted_id)

    # Create JWT token payload.
    token_payload = {
        "sub": user_id,
        "email": user_data["email"],
        "provider": provider
    }
    jwt_token = create_jwt_token(token_payload, timedelta(minutes=ACCESS_TOKEN_EXPIRE))

    # Return JSON response with token details.
    return JSONResponse(content=Token(
        access_token=jwt_token,
        expires_in=ACCESS_TOKEN_EXPIRE * 60  # in seconds
    ).model_dump())
