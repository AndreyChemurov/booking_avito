from fastapi import FastAPI
import os


app = FastAPI()

connection_params = {
    "dbname": os.environ.get('POSTGRES_DATABASE'),
    "user": os.environ.get('POSTGRES_USER'),
    "password": os.environ.get('POSTGRES_PASSWORD'),
    "host": os.environ.get('POSTGRES_HOST'),
    "port": 5432
}
