from fastapi import FastAPI, Request
import configparser
from models import Database, Book, GiveRequest
from aiohttp_requests import requests
import aiohttp


config = configparser.RawConfigParser()
config.read('config.ini')


app = FastAPI()
db = Database()


@app.get("/books/")
async def get_free_books():
    books = await db.get_free_books()
    return books


@app.get("/busy_books/")
async def get_free_books():
    books = await db.get_busy_books()
    return books


@app.post("/add_book")
async def add_book(book: Book):
    try:
        result = await db.add_book(book)
        return {'result': result}
    except Exception as e:
        return {'result': False, 'error': str(e)}


@app.post("/del_book/<str:book_id>")
async def del_book(book_id):
    result = await db.delete_book(book_id)
    return {'result': result}


@app.post("/give_book")
async def give_book(request: GiveRequest):
    result = await db.give_book(request)
    return {'result': result}


@app.post("/send_report")
async def send_report():
    response = await requests.post('http://0.0.0.0:8888/send_report', auth=aiohttp.BasicAuth('user', 'password'))  # хотел сделать какую-то авторизацию на сервисе но влом
    json = await response.json()
    return {'result': True, 'response': json}


@app.get("/auth")
async def auth():
    return {'status': True}
