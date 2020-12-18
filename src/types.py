from pydantic import BaseModel
from typing import (
    Optional,
    List,
    Dict
)
from datetime import date


class RequestHotelCreate(BaseModel):
    """ Документация (параметр: объяснение дефолтного значения) """

    description: Optional[str] = None
    price: Optional[int] = None


class RequestHotelRemove(BaseModel):
    """ Документация (параметр: объяснение дефолтного значения) """

    identifier: Optional[int] = None


class RequestHotelList(BaseModel):
    """ Документация (параметр: объяснение дефолтного значения) """

    sort: Optional[str] = None


class RequestBookingsCreate(BaseModel):
    """ Документация (параметр: объяснение дефолтного значения) """

    identifier: Optional[int] = None
    date_start: Optional[date] = date(1970, 1, 1)
    date_end: Optional[date] = date(1970, 1, 1)


class RequestBookingsRemove(BaseModel):
    """ Документация (параметр: объяснение дефолтного значения) """

    identifier: Optional[int] = None


class RequestBookingsList(BaseModel):
    """ Документация (параметр: объяснение дефолтного значения) """

    identifier: Optional[int] = None


class ResponseHotelCreate:
    """ Документация """
    def __init__(self, identifier: int):
        self.identifier = identifier


class ResponseHotelRemove:
    """ Документация """
    def __init__(self, identifier: int):
        self.identifier = identifier


class ResponseHotelList:
    """ Документация """
    def __init__(self, rooms: List[Dict]):
        self.rooms = rooms


class ResponseBookingsCreate:
    """ Документация """
    def __init__(self, identifier: int):
        self.identifier = identifier


class ResponseBookingsRemove:
    """ Документация """
    def __init__(self, identifier: int):
        self.identifier = identifier


class ResponseBookingsList:
    """ Документация """
    def __init__(self, bookings: List[Dict]):
        self.bookings = bookings
