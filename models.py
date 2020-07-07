from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson.objectid import ObjectId, InvalidId
import motor.motor_asyncio
import logging


class OID(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return ObjectId(str(v))
        except InvalidId:
            raise ValueError("Not a valid ObjectId")


class GiveRequest(BaseModel):
    book_id: OID = Field()
    given_by: OID = Field()
    taken_by: OID = Field()

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            ObjectId: lambda oid: str(oid),
        }


class Category(BaseModel):
    _id: OID
    name: str = ''


class User(BaseModel):
    _id: OID
    name: str = ''
    signup_ts: Optional[datetime] = None
    role: str = None
    email: str = ''
    password: str = ''

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            ObjectId: lambda oid: str(oid),
        }


class Book(BaseModel):
    _id: OID
    title: str = None
    categories: Optional[List[OID]] = None
    assign_ts: Optional[datetime] = None
    taken_by: OID = None
    given_by: OID = None
    content: str = ''

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            ObjectId: lambda oid: str(oid),
        }


class Database:

    def __init__(self):
        self.mongo_conn = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://hornet:gnuIjj8EdK1tXZ6U@cluster0.ofprt.mongodb.net")
        self.db = self.mongo_conn['library']

    async def _parse_books(self, cur) -> List[Book]:
        parsed_books = [Book(**book) for book in await cur.to_list(length=10000)]
        return parsed_books

    async def get_free_books(self) -> List[Book]:
        # Получение книги по ID
        cursor = self.db.books.find({'taken_by': None})
        books = await self._parse_books(cursor)
        return books

    async def get_busy_books(self) -> List[Book]:
        # Получение книги по ID
        cursor = self.db.books.find({'taken_by': {'$ne': None}})
        books = await self._parse_books(cursor)
        return books

    async def give_book(self, request: GiveRequest) -> Optional[Book]:
        """
        Выдать книгу
        :return:
        """
        if self.is_admin(request.given_by):
            book = await self.db.books.find_one({'_id': request.book_id})
            book = Book(**book)
            book.assign_ts = datetime.now()
            book.given_by = request.given_by
            book.taken_by = request.taken_by
            await self.db.books.replace_one({'_id': request.book_id}, book.dict())
            return book
        else:
            raise Exception('not Admin')

    async def is_admin(self, user_id: OID) -> bool:
        """
        Проверка права на выдачу книг
        :param user_id:
        :return:
        """
        user = await self.db.users.find_one({'_id': user_id})
        if user['role'] == 'admin':
            return True
        return False

    async def add_book(self, book: Book) -> bool:
        """
        Добавить книгу в базу
        :param book:
        :return:
        """
        await self.db.books.insert_one(book.dict())
        return True

    async def delete_book(self, book_id: OID) -> bool:
        # Удаление книги
        await self.db.books.delete_one({'_id': book_id})
        return True
