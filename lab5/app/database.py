from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from typing import Optional

MONGO_DETAILS = "mongodb://admin:password@localhost:27017"
DATABASE_NAME = "library"

client: Optional[AsyncIOMotorClient] = None
db: Optional[AsyncIOMotorDatabase] = None

async def connect_to_mongo():
    global client, db
    print("Підключення до MongoDB...")
    client = AsyncIOMotorClient(MONGO_DETAILS)
    db = client[DATABASE_NAME]
    try:
        await client.admin.command('ping')
        print(f"Успішно підключено до MongoDB! База даних: {db.name}")
    except Exception as e:
        print(f"Не вдалося підключитися до MongoDB: {e}")
        client = None
        db = None

async def close_mongo_connection():
    global client
    if client:
        print("Закриття з'єднання з MongoDB...")
        client.close()
        print("З'єднання з MongoDB закрито.")

def get_db_collection(collection_name: str) -> AsyncIOMotorCollection:
    if db is None:
        raise ConnectionError("З'єднання з базою даних не встановлено.")
    return db[collection_name]

async def get_book_collection() -> AsyncIOMotorCollection:
    if db is None:
        await connect_to_mongo()
        if db is None:
             raise ConnectionError("Не вдалося встановити з'єднання з базою даних для отримання колекції.")
    return db.get_collection("books")
