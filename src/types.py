from pydantic import BaseModel
from typing import (
    Optional,
    List,
    Dict
)
from datetime import date


class RequestHotelCreate(BaseModel):
    """ Объект запроса пути "/hotel/create"
    Включает в себя:
        - Текстовое описание комнаты.
        - Цена за ночь.
    """

    description: Optional[str] = None
    price: Optional[int] = None


class RequestHotelRemove(BaseModel):
    """ Объект запроса пути "/hotel/remove"
    Включает в себя:
        - ID комнаты отеля.
    """

    identifier: Optional[int] = None


class RequestHotelList(BaseModel):
    """ Объект запроса пути "/hotel/list"
    Включает в себя:
        - Параметр сортировки: "price", "asc_date" или "desc_date".
    """

    sort: Optional[str] = None


class RequestBookingsCreate(BaseModel):
    """ Объект запроса пути "/bookings/create"
    Включает в себя:
        - ID комнаты отеля для брони.
        - Дату начала (по дефолту - 1970/01/01).
        - Дату конца (по дефолту - 1970/01/01)
    """

    identifier: Optional[int] = None
    date_start: Optional[date] = date(1970, 1, 1)
    date_end: Optional[date] = date(1970, 1, 1)


class RequestBookingsRemove(BaseModel):
    """ Объект запроса пути "/bookings/remove"
    Включает в себя:
        - ID брони.
    """

    identifier: Optional[int] = None


class RequestBookingsList(BaseModel):
    """ Объект запроса пути "/bookings/list"
    Включает в себя:
        - ID номера отеля.
    """

    identifier: Optional[int] = None


class ResponseHotelCreate:
    """ Объект ответа пути /hotel/create
    Возвращает:
        - ID созданной комнаты отеля.
    """

    def __init__(self, identifier: int):
        self.identifier = identifier


class ResponseHotelRemove:
    """ Объект ответа пути /hotel/remove
    Возвращает:
        - ID удаленной комнаты отеля.
    """

    def __init__(self, identifier: int):
        self.identifier = identifier


class ResponseHotelList:
    """ Объект ответа пути /hotel/list
    Возвращает:
        - Список (IDs) комнат отеля.
    """

    def __init__(self, rooms: List[Dict]):
        self.rooms = rooms


class ResponseBookingsCreate:
    """ Объект ответа пути /bookings/create
    Возвращает:
        - ID созданной брони.
    """

    def __init__(self, identifier: int):
        self.identifier = identifier


class ResponseBookingsRemove:
    """ Объект ответа пути /bookings/remove
    Возвращает:
        - ID удаленной брони.
    """

    def __init__(self, identifier: int):
        self.identifier = identifier


class ResponseBookingsList:
    """ Объект ответа пути /bookings/list
    Возвращает:
        - Список броней (ID брони, дата начала, дата окончания) для комнаты.
    """

    def __init__(self, bookings: List[Dict]):
        self.bookings = bookings
