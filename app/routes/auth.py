""""
    THIS IS THE ENDPOINT
    runs as localhost:8000/auth
    Details:
    This following API endpoint authenticates user to a github platform
"""

from fastapi import APIRounter, Request, HTTPException #type: ignore
from fastapi.responses import RedirectResponse #type: ignore
from app.oauth import oauth

# Initialize router
router = APIRounter()

#create endpoint for authentication

@router.get("/auth") #This means router would get the GET request from /auth endpoint.
async def auth(request: Request, provider: str):
    """
    Initiate OAuth2 login flow.
    Example: GET /auth?provider=google
    """
    if provider not in ["github"]:
        raise HTTPException(status_code=400, detail="Unlisted provider")
        #This code means: If you use something besides github it would fail and provided status code 400:
        #More about status codes on: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    redirect_uri = request.url_for("token_callback", provider=provider)
    client = oauth.create_client(provider)
    return await client.authorize_redirect(request, redirect_uri)

"""""
GET request is the REST API type of request which retrieves information and provides it a user cookie.
There are 4 types basic requests aswell as
POST: User sends info 
Update/put: Changes info
Patch: Add additional info to already existed one
Delete: Deletes request
"""