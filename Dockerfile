FROM python:3.8.1-buster

EXPOSE 8000

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD uvicorn main:app --reload --host=0.0.0.0 && nameko run http_service --config service_conf.yaml