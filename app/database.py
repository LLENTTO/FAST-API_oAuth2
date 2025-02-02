""""
This is Database configuration for mongoDB: 

MongoDB is NoSQL database. You can configure this file if you want to use POSTGRESQL
"""

from motor.motor_asyncio import AsyncIOMotorClient # type: ignore
from config import MONGO_URI #Imports the URI for mongo to use (ps: it would run either on local machine or docker machine)

#Configure URI
client = AsyncIOMotorClient(MONGO_URI)
db = client.get_default_database()