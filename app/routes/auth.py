"""
THIS IS THE ENDPOINT
Runs as localhost:8000/auth

Details:
This API endpoint initiates the OAuth2 login flow for a GitHub account.
"""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from app.oauth import oauth

# Initialize router
router = APIRouter()

@router.get("/auth")
async def auth(request: Request, provider: str):
    """
    Initiate OAuth2 login flow.
    
    Example: GET /auth?provider=github
    
    Raises:
        HTTPException: If the provider is not supported.
    
    Returns:
        A redirect response to the OAuth provider's authorization URL.
    """
    if provider not in ["github"]:
        raise HTTPException(status_code=400, detail="Unlisted provider")
    
    # Generate the redirect URI for the token callback endpoint.
    # Make sure the token callback endpoint is defined with a corresponding parameter,
    # for example, as /token/{provider} with name "token_callback".
    redirect_uri = request.url_for("token_callback", provider=provider)
    
    client = oauth.create_client(provider)
    return await client.authorize_redirect(request, redirect_uri)
