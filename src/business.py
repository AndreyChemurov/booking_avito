from fastapi import HTTPException
from datetime import date
from typing import (
    List,
    Dict
)


class Database:
    pass


def hotel_create(description: str, price: int) -> int:
    """ Метод создает новую запись в таблице  """

    # TODO: raise'ить исключения на уровне бизнес-логики
    # TODO: [описание, цена, время в юникс создания]

    # TODO: СОЗДАТЬ ИНДЕКСЫ

    return 1    # Идентификатор возвращается только в случае успеха, иначе - exception


def hotel_remove(identifier: int) -> int:
    """ Документация """

    # TODO: удаляет номер и все брони
    # TODO: ID должен существовать

    # TODO: СОЗДАТЬ ИНДЕКСЫ

    return 1


def hotel_list(sort: str) -> List[Dict]:
    """ Документация """
    return [{}]


def bookings_create(identifier: int, date_start: date = None, date_end: date = None) -> int:
    """ Документация """

    # TODO: ID должен существовать

    # TODO: СОЗДАТЬ ИНДЕКСЫ

    return 1


def bookings_remove(identifier: int) -> int:
    """ Документация """

    # TODO: ID должен существовать

    # TODO: СОЗДАТЬ ИНДЕКСЫ

    return 1


def bookings_list(identifier: int) -> List[Dict]:
    """ Документация """

    # TODO: ID должен существовать
    # TODO: как сортировать брони по дате начала? RETURNING SORTED? (надо в БД делать)

    # TODO: СОЗДАТЬ ИНДЕКСЫ

    return [{}]
