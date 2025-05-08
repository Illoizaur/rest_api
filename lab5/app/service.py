from typing import List, Optional
from bson import ObjectId

# Я спробував заставити працювати ось цю штуковину внизу,але чомусь вона
# максимально відмовляється до співпраці
# Тому замінено на банальний стрінг
#from pydantic_mongo import PydanticObjectId

from app.models import BookCreate, BookUpdate, BookInDB
from app.database import get_book_collection


async def create_book(book_data: BookCreate) -> BookInDB:
    collection = await get_book_collection()
    book_dict = book_data.model_dump()
    result = await collection.insert_one(book_dict)
    created_book_doc = await collection.find_one({"_id": result.inserted_id})
    if created_book_doc:
        created_book_doc["_id"] = str(created_book_doc["_id"])
        return BookInDB(**created_book_doc)
    raise Exception("Помилка при створенні книги: не вдалося отримати створений запис.")


async def get_all_books(skip: int = 0, limit: int = 100) -> List[BookInDB]:
    collection = await get_book_collection()
    books_cursor = collection.find({}).skip(skip).limit(limit)
    books_list = []
    async for book_doc in books_cursor:
        book_doc["_id"] = str(book_doc["_id"])
        books_list.append(BookInDB(**book_doc))
    return books_list


async def get_book_by_id(book_id: str) -> Optional[BookInDB]:
    collection = await get_book_collection()
    object_id = ObjectId(book_id)
    book_doc = await collection.find_one({"_id": object_id})
    if book_doc:
        book_doc["_id"] = str(book_doc["_id"])
        return BookInDB(**book_doc)
    return None


async def update_book(book_id: str, book_data: BookUpdate) -> Optional[BookInDB]:
    collection = await get_book_collection()
    update_data_dict = book_data.model_dump(exclude_unset=True)

    if not update_data_dict:
        return await get_book_by_id(book_id)

    object_id = ObjectId(book_id)
    result = await collection.update_one(
        {"_id": object_id},
        {"$set": update_data_dict}
    )
    if result.modified_count == 1:
        updated_book_doc = await collection.find_one({"_id": object_id})
        if updated_book_doc:
            updated_book_doc["_id"] = str(updated_book_doc["_id"])
            return BookInDB(**updated_book_doc)
    return await get_book_by_id(book_id)


async def delete_book(book_id: str) -> bool:
    collection = await get_book_collection()
    object_id = ObjectId(book_id)
    result = await collection.delete_one({"_id": object_id})
    return result.deleted_count > 0
