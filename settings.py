from fastapi import FastAPI
import os


# TODO (Документация): что за приложение?
app = FastAPI()

# TODO (Документация): что за параметры?
connection_params = {
    "database": os.environ.get('POSTGRES_DATABASE'),
    "user": os.environ.get('POSTGRES_USER'),
    "password": os.environ.get('POSTGRES_PASSWORD'),
    "host": "localhost",
    "port": 5432
}
