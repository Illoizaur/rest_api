from pydantic import BaseModel, Field, ConfigDict
# from pydantic_mongo import PydanticObjectId # Не арбайтає
from typing import Optional

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, description="Назва книги")
    author: str = Field(..., min_length=1, description="Автор книги")
    year: Optional[int] = Field(None, gt=0, description="Рік видання")
    isbn: Optional[str] = Field(None, description="ISBN номер книги")
    genre: Optional[str] = Field(None, description="Жанр книги")

    model_config = ConfigDict(
        populate_by_name=True,
    )

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    author: Optional[str] = Field(None, min_length=1)
    year: Optional[int] = Field(None, gt=0)
    isbn: Optional[str] = None
    genre: Optional[str] = None

    model_config = ConfigDict()

class BookInDB(BookBase):
    id: str = Field(alias="_id")
