from pymongo import MongoClient
import os
from dotenv import load_dotenv
import ssl
import certifi

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where()
)

db = client["nirmatriDB"]
