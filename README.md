GET http://0.0.0.0:8000/books
получить свободные книги


GET http://0.0.0.0:8000/busy_books
получить  книги на руках


POST http://0.0.0.0:8000/give_book  выдать книгу

{
	"book_id": "5f0381075d527d315a86efb9",
	"given_by": "5f038611469f7522c2a80835",
	"taken_by": "5f0386ef469f7522c2a80836"
}


http://0.0.0.0:8000/add_book  добавить книгу в базу
{
	"title":"451° по Фаренгейту",
	"content": "какой-то контент:)"
}



Запуск через докер:

docker-compose build

docker-compose up -d



Запуск локально

pip install -r requirements.txt

uvicorn main:app --reload --host=0.0.0.0 && nameko run http_service --config service_conf.yaml