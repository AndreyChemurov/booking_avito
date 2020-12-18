from fastapi import HTTPException
from datetime import date

from settings import app
from .types import (
    # Классы запросов для хендлеров отеля
    RequestHotelCreate,
    RequestHotelRemove,
    RequestHotelList,

    # Классы запросов для хендлеров брони
    RequestBookingsCreate,
    RequestBookingsRemove,
    RequestBookingsList,

    # Классы ответов от хендлеров отеля
    ResponseHotelCreate,
    ResponseHotelRemove,
    ResponseHotelList,

    # Классы ответов от хендлеров брони
    ResponseBookingsCreate,
    ResponseBookingsRemove,
    ResponseBookingsList
)

from .errors import (
    HTTP_400_WRONG_PARAMS
)

from .business import (
    # Методы бизнес-логики хендлеров отеля
    hotel_create as h_create,
    hotel_remove as h_remove,
    hotel_list as h_list,

    # Методы бизнес-логики хендлеров брони
    bookings_create as b_create,
    bookings_remove as b_remove,
    bookings_list as b_list
)


@app.post("/hotel/create")
def hotel_create(r: RequestHotelCreate) -> ResponseHotelCreate:
    """ Метод добавления номера отеля.

    Атрибуты:
        - description [str]: текстовое описание.
        - price [int]: цена за ночь.
    Возвращаемые значения:
        - identifier [int]: ID номера отеля.
    """

    # Проверить валидность атрибутов запроса
    if any([
        r.description is None,
        r.price is None,
        isinstance(r.price, int) and r.price <= 0
    ]):
        raise HTTPException(
            status_code=400,
            detail=HTTP_400_WRONG_PARAMS
        )

    # Бизнес-логика возвращает идентификатор номера отеля
    identifier = h_create(r.description, r.price)

    return ResponseHotelCreate(identifier=identifier)


@app.post("/hotel/remove")
def hotel_remove(r: RequestHotelRemove) -> ResponseHotelRemove:
    """ Метод удаления номера отеля и всех его броней.

    Атрибуты:
        - identifier [int]: ID номера отеля для удаления.
    Возвращаемые значения:
        - identifier [int]: ID удаленного номера отеля.
    """

    # Проверить валидность атрибутов запроса
    if any([
        r.identifier is None,
        isinstance(r.identifier, int) and r.identifier <= 0
    ]):
        raise HTTPException(
            status_code=400,
            detail=HTTP_400_WRONG_PARAMS
        )

    # Бизнес-логика возвращает идентификатор удаленного номера отеля
    identifier = h_remove(r.identifier)

    return ResponseHotelRemove(identifier=identifier)


@app.post("/hotel/list")
def hotel_list(r: RequestHotelList) -> ResponseHotelList:
    """ Метод получения списка номеров отеля.

    Атрибуты:
        - sort [str]: параметр сортировки.
    Возвращаемые значения:
        - rooms [list of dicts]: список номеров отеля.
    """

    # Проверить валидность атрибутов запроса
    if any([
        r.sort is None,

        # Параметры сортировки могут быть:
        #   1. "asc_date": сортировка по дате добавления (по возрастанию).
        #   2. "desc_date": сортировка по дате добавления (по убыванию).
        #   3. "price": сортировка по цене.
        r.sort not in ("asc_date", "desc_date", "price")
    ]):
        raise HTTPException(
            status_code=400,
            detail=HTTP_400_WRONG_PARAMS
        )

    # Бизнес-логика возвращает список номеров отеля
    # Каждая комната состоит из:
    #   1. "room_id": ID номера отеля.
    #   2. "description": текстовое описание.
    #   3. "price": цена за ночь.
    #   4. "date_created": дата добавления номера в отель.
    rooms = h_list(r.sort)

    return ResponseHotelList(rooms=rooms)


@app.post("/bookings/create")
def bookings_create(r: RequestBookingsCreate) -> ResponseBookingsCreate:
    """ Метод добавления брони.

    Атрибуты:
        - identifier [int]: ID существующего номера отеля.
        - date_start [date]: дата начала брони.
        - date_end [date]: дата окончания брони.
    Возвращаемые значения:
        - identifier [int]: ID брони.
    """

    # Проверить валидность атрибутов запроса
    if any([
        r.identifier is None,
        r.date_start is None,
        r.date_end is None,

        # Нельзя зарбронировать номер раньше, чем выселиться из него
        isinstance(r.identifier, int) and r.identifier <= 0,
        (
                not isinstance(r.date_start, date) and
                not isinstance(r.date_end, date) and
                r.date_end < r.date_start
        ),
        # Нельзя зарбронировать номер раньше, чем выселиться из него
    ]):
        raise HTTPException(
            status_code=400,
            detail=HTTP_400_WRONG_PARAMS
        )

    # Бизнес-логика возвращает идентификатор созданной брони
    identifier = b_create(r.identifier, r.date_start, r.date_end)

    return ResponseBookingsCreate(identifier=identifier)


@app.post("/bookings/remove")
def bookings_remove(r: RequestBookingsRemove) -> ResponseBookingsRemove:
    """ Метод удаления брони.

    Атрибуты:
        - identifier [int]: ID брони.
    Возвращаемые значения:
        - identifier [int]: ID удаленной брони.
    """

    # Проверить валидность атрибутов запроса
    if any([
        r.identifier is None,
        isinstance(r.identifier, int) and r.identifier <= 0
    ]):
        raise HTTPException(
            status_code=400,
            detail=HTTP_400_WRONG_PARAMS
        )

    # Бизнес-логика возвращает идентификатор удаленной брони
    identifier = b_remove(r.identifier)

    return ResponseBookingsRemove(identifier=identifier)


@app.post("/bookings/list")
def bookings_list(r: RequestBookingsList) -> ResponseBookingsList:
    """ Метод получения списка броней номера отеля.

    Атрибуты:
        - identifier [int]: ID номера отеля.
    Возвращаемые значения:
        - bookings [list of dicts]: список бронирований.
    """

    # Проверить валидность атрибутов запроса
    if any([
        r.identifier is None,
        isinstance(r.identifier, int) and r.identifier <= 0
    ]):
        raise HTTPException(
            status_code=400,
            detail=HTTP_400_WRONG_PARAMS
        )

    # Бизнес-логика возвращает список броней номера отеля
    # Каждая бронь имеет:
    #   1. идентификатор
    #   2. дата начала
    #   3. дата окончания
    # Все брони отстортированы по дате начала
    bookings = b_list(r.identifier)

    return ResponseBookingsList(bookings=bookings)
