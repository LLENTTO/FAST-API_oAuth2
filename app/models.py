""""
         This file creates a Model for User and Token
         Basically it says how the data would be stored on database
         It would configure the user and what credentials does it have
"""


from pydantic import BaseModel, EmailStr
from typing import Optional

# Creates model for user. Like it would have the id, email, fullname and provider
class User(BaseModel):
    id: str
    email: EmailStr
    full_name: Optional[str] = None
    provider: str

# This creates token. Basically its a session containing user credentials for certain amount of time
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int