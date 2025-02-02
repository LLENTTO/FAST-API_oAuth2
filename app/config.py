''''
This is config file: it initializes nessesary configurations for oauth logging 
'''

import os
from dotenv import load_dotenv # type: ignore

# Intializing dotenv (ps: read about .env files if you dont know what are them)
load_dotenv()

# settings api endpoints for database
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
SECRET_KEY = os.getenv("secret-key", "password1337")

ALGORITHM="HS256" #idk read about it
ACCESS_TOKEN_EXPIRE=120 #its 120 minutes, or 2 hours. configure if you want to change its behavior


"""
This inializes the oauth id: they are created on seperate accounts. I will provide you the .env file if you contact me
"""

GITHUB_CLIENT_ID=os.getenv("Github_client-id", "")
GITHUB_CLIENT_SECRET=os.getenv("Github_clien-secret", "")