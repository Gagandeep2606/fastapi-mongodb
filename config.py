from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv

MONGO_URL = os.getenv("MONGO_URL")

client =MongoClient(MONGO_URL)
db = client["practice_db"]
users = db["users"]
cities = db["cities"]

sales_db = client["sales_db"]
orders = sales_db["orders"]
