import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "prior_authorization")

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

db_config = MongoDB()

async def connect_to_mongo():
    if not MONGODB_URI:
        logging.error("MONGODB_URI is not configured in backend/.env")
        return
        
    logging.info("Connecting to MongoDB...")
    db_config.client = AsyncIOMotorClient(MONGODB_URI)
    db_config.db = db_config.client[MONGODB_DATABASE]
    
    # Try connecting
    try:
        await db_config.client.admin.command('ping')
        logging.info("Successfully connected to MongoDB!")
    except Exception as e:
        logging.error(f"Error connecting to MongoDB: {e}")

async def close_mongo_connection():
    if db_config.client:
        logging.info("Closing MongoDB connection...")
        db_config.client.close()

def get_db():
    return db_config.db
