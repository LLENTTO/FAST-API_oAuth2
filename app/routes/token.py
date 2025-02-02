""""
    THIS IS ANOTHER ENDPOINT
    This router provides the /token endpoint, which acts as the callback endpoint
    It exchanges the authorization code for an access token, retrieves user information, creates a JWT (with a 2‑hour expiration), upserts the user in MongoDB, and returns the JWT.
"""

from fastapi import APIRouter, Request, HTTPException #type: ignore
from fastapi.responses import JSONResponse #type: ignore
import jwt #type:ignore
from datetime import datetime, timedelta
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE
from oauth import oauth
from database import db
from models import Token
from bson import ObjectId #type: ignore

# Add router
router = APIRouter()

def create_jwt_token(data: dict, expires_delta: timedelta = None):
    """"
    Creates a Json web token with payload for expiration
    """
    to_encode = data.copy()
    expire = datetime.now(datetime.timezone.utc) + (expires_delta) or timedelta(minutes=ACCESS_TOKEN_EXPIRE) #Basically token expiration time
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

"""""
Quick explanation to create_jwt_token function

This creates a token. Token is nessesary for handling a specific key info of user and it contains in session with time expiration for secure purposes.

Learn more about JsonWebTokens
"""

@router.get("/token", name="token_callback")
async def token_callback(request: Request, provider: str):
    """"
    Endpoint for callback
    This one checks and reddirects to this endpoint after a successfull login
    """
    if provider not in ["github"]: #ensures you are logging in to github oauth
        raise HTTPException(status_code=400, detail="Unsupported provider (Bad Request)")
    
    client = oauth.create_client(provider)


    # So this block of code ensures if users was successfully authorized without any error
    try:
        token = await client.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to authorize: Bad request") from e 

    user_info = None
    if provider == "github":
        # Fetch user profile
        res = await client.get("user", token=token)
        user_info = res.json()

        #Try fetching emails if there are no emails
        if not user_info.get("email"):
            emails_resp = await client.get("user/emails", token=token)
            emails = emails_resp.json()
            primary_emails = [email for email in emails if email.get("primary") and email.get("verified")]

            #retrives email info
            if primary_emails:
                user_info["email"] = primary_emails[0]["email"]
            elif emails:
                user_info["email"] = emails[0]["email"]
    
    #Check if theres no users and raise error
    if not user_info or not user_info.get("email"):
        raise HTTPException(status_code=400, details="Fail in getting emails") #basically bad request if there are no emails
    
    # Prepare user data
    user_data = {
        "email": user_info.get("email"),
        "full_name": user_info.get("name") or user_info.get("login"),
        "provider": provider
    }

    # Push info to the database
    users_collection = db.get_collection("users")
    existing_user= await users_collection.find_one({"email": user_data["email"]})
    # If user exists simply retrieve the id
    if existing_user:
        user_id = str(existing_user["_id"])
    else:
        #basically if it creates a new user it creates a new user in the collection
        result = await users_collection.insert_one(user_data)
        user_id = str(result.inserted_id)

    #create JWT payload
    """"
    In JSON Web Tokens (JWT), the token payload is the part of the token that contains the claims. Claims are statements about an entity (typically, the user) and additional metadata. The payload is a JSON object that is base64url-encoded and forms the second part of the JWT structure
    """
    token_payload = {
        "sub":user_id,
        "email": user_data["email"],
        "provider": provider
    }

    jwt_token = create_jwt_token(token_payload, timedelta (minutes=ACCESS_TOKEN_EXPIRE))
    
    token_response = Token(
        access_token=jwt_token,
        expires_in=ACCESS_TOKEN_EXPIRE * 60  # in seconds
    )
    return JSONResponse(content=token_response.dict())