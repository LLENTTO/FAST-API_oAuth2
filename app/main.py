from fastapi import FastAPI # type: ignore
from app.routes import auth, token
from starlette.middleware.sessions import SessionMiddleware #type: ignore
import os
from dotenv import load_dotenv # type: ignore
load_dotenv()

app = FastAPI()

key= os.getenv("secret-key", "password1337")

app.add_middleware(SessionMiddleware, secret_key=key)

app.include_router(auth.router)
app.include_router(token.router)