from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import get_settings

settings = get_settings()

class MongoClientManager:
    client: AsyncIOMotorClient = None
    db = None

    @classmethod
    def connect(cls):
        cls.client = AsyncIOMotorClient(settings.MONGO_URL)
        cls.db = cls.client[settings.MONGO_DB]

    @classmethod
    def close(cls):
        if cls.client:
            cls.client.close()

mongo_manager = MongoClientManager()

def get_mongo_db():
    if mongo_manager.db is None:
        mongo_manager.connect()
    return mongo_manager.db
