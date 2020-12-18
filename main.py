import uvicorn
import json
from settings import app
from src.transport import (
    hotel_create as h_create,
    hotel_remove as h_remove,
    hotel_list as h_list,

    bookings_create as b_create,
    bookings_remove as b_remove,
    bookings_list as b_list
)
from setup_database import create_tables


def hotel_create():
    """ Метод добавления номера отеля """
    return h_create()


def hotel_remove():
    """ Метод удаления номера отеля и всех его броней """
    return h_remove()


def hotel_list():
    """ Метод получения списка номеров отеля """
    return h_list()


def bookings_create():
    """ Метод добавления брони """
    return b_create()


def bookings_remove():
    """ Метод удаления брони """
    return b_remove()


def bookings_list():
    """ Метод получения списка броней номера отеля """
    return b_list()


if __name__ == '__main__':
    # TODO (Документация): добавить что за запуск приложения и как этот запуск работает

    file = open('is_db_created.json', 'r')
    is_created = json.load(file)
    file.close()

    if not is_created['tables_created']:

        # Если таблицы успешно созданы, то изменения записываются в файл
        if create_tables():
            print("Created")
            file = open('is_db_created.json', 'w')
            json.dump({"tables_created": True}, file)

            file.close()

    uvicorn.run(app=app, host="0.0.0.0", port=9000)
