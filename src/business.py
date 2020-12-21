from fastapi import HTTPException
from datetime import date
from typing import (
    List,
    Dict
)
import psycopg2

from .errors import (
    HTTP_500_DATABASE_ERROR,
    HTTP_500_DATABASE_EMPTY_BOOKINGS_LIST
)

""" connection_params - переменные среды откружения для подключения к БД.
    1. Имя БД
    2. Пользователь
    3. Пароль
    4. Хост
    5. Порт (константа, не env_var)
"""
from setup_database import connection_params


def run_query(query: str):
    """ Функция открывает соединение с БД и делает запрос

    Аргументы:
        - query [str]: запрос в БД.
    """

    connection, cursor = None, None
    value = 0

    try:
        connection = psycopg2.connect(**connection_params)
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()

        # Получение значение от выражения RETURNING
        value = cursor.fetchall()

        cursor.close()
    except (Exception, psycopg2.DatabaseError):
        raise HTTPException(
            status_code=500,
            detail=HTTP_500_DATABASE_ERROR
        )
    finally:
        if not connection.closed:
            connection.close()
        if not cursor.closed:
            cursor.close()

    return value


def get_database_value(query: str):
    """ Функция вброса ошибки в случае, если значение значение достать не удалось или оно дефолтное (0) """

    database_value = run_query(query)   # list of one tuple

    if not database_value or database_value[0][0] == 0:
        raise HTTPException(
            status_code=500,
            detail=HTTP_500_DATABASE_ERROR
        )

    return database_value[0][0]


def hotel_create(description: str, price: int) -> int:
    query = f"INSERT INTO hotel (description, price) VALUES (\'{description}\', {price}) RETURNING room_id;"

    database_value = get_database_value(query)

    return database_value


def hotel_remove(identifier: int) -> int:
    query = f"DELETE FROM bookings WHERE room_id = {identifier};" \
            f"DELETE FROM hotel WHERE room_id = {identifier} RETURNING room_id;"

    database_value = get_database_value(query)

    return database_value


def hotel_list(sort: str) -> List[Dict]:
    # Мапа соотношений запросов к БД и JSON
    sort_variations = {
        "price": "price",
        "asc_date": "created_at",
        "desc_date": "created_at DESC"
    }

    query = f"SELECT room_id FROM hotel " \
            f"ORDER BY {sort_variations[sort]};"

    database_value = run_query(query)   # list of tuples

    database_value = [{"room_id": value[0]} for value in database_value]

    return database_value


def bookings_create(identifier: int, date_start: date = None, date_end: date = None) -> int:
    query = f"INSERT INTO bookings (" \
            f"room_id, date_start, date_end) " \
            f"SELECT room_id, \'{date_start}\', \'{date_end}\' " \
            f"FROM hotel " \
            f"WHERE room_id = {identifier} " \
            f"RETURNING booking_id;"

    database_value = get_database_value(query)

    return database_value


def bookings_remove(identifier: int) -> int:
    query = f"DELETE FROM bookings WHERE booking_id = {identifier} RETURNING booking_id;"

    database_value = get_database_value(query)

    return database_value


def bookings_list(identifier: int) -> List[Dict]:
    query = f"SELECT booking_id, date_start, date_end " \
            f"FROM bookings " \
            f"WHERE room_id = {identifier} " \
            f"ORDER BY date_start;"

    database_value = run_query(query)

    if not database_value:
        raise HTTPException(
            status_code=500,
            detail=HTTP_500_DATABASE_EMPTY_BOOKINGS_LIST
        )

    database_value = [
        {
            "booking_id": value[0],
            "date_start": value[1].strftime("%Y-%m-%d"),
            "date_end": value[2].strftime("%Y-%m-%d")
        }
        for value in database_value
    ]

    return database_value
