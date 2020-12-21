# Сервис для управления номерами отелей и бронированиями: Авито.Недвижимость

## Информация
- Приложение работает на порту ```9000```
- Все запросы выполняются через POST методы с JSON телом.
- На транспортном уровне выполняется проверка валидности переданных в теле метода аргументов. Хендлеры формируют JSON-ответ на основе строго-типизировнных данных.
- На бизнес уровне создаются запросы и коннекшены с базой данных.
- Каждый возвращаемый статус код, если он 5xx или 4xx, соответствует своему уровню абстракции.</br></br>

Стек технологий:
- Python 3.7
- Фреймворк FastAPI
- PostgreSQL

Я использую Linux Debian

## Запуск приложения
```bash
git clone https://github.com/AndreyChemurov/booking_avito.git
cd booking_avito/
[sudo] docker-compose up
```

## Примеры запросов и ответов
<i><strong>Каждый пример кода содержит по 2 функции: первая - функция транспортного уровня, вторая - бизнес логики.</strong></i></br>

**Запрос на добавление нового номера в отеле:**

![Screenshot_20201221_171008](https://user-images.githubusercontent.com/58785926/102785729-7a973600-43af-11eb-9827-da78b63ff05e.png)

```python
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
    identifier = int(h_create(r.description, r.price))

    return ResponseHotelCreate(identifier=identifier)

def hotel_create(description: str, price: int) -> int:
    query = f"INSERT INTO hotel (description, price) VALUES (\'{description}\', {price}) RETURNING room_id;"

    database_value = get_database_value(query)

    return database_value
```

**Запрос на удаление номера и всех его броней:**

![Screenshot_20201221_171701](https://user-images.githubusercontent.com/58785926/102786318-5c7e0580-43b0-11eb-87fe-b1330ed28505.png)

```python
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
    identifier = int(h_remove(r.identifier))

    return ResponseHotelRemove(identifier=identifier)

def hotel_remove(identifier: int) -> int:
    query = f"DELETE FROM bookings WHERE room_id = {identifier};" \
            f"DELETE FROM hotel WHERE room_id = {identifier} RETURNING room_id;"

    database_value = get_database_value(query)

    return database_value
```

**Запрос на список номеров отеля:**

<i><strong>Дата создания задается дефолтным значением - сегдняшняя.</strong></i></br>

![Screenshot_20201221_171936](https://user-images.githubusercontent.com/58785926/102786528-b7176180-43b0-11eb-9767-1e0b72525a32.png)

```python
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

    # Бизнес-логика возвращает список номеров отеля (лист из room_id)
    rooms = h_list(r.sort)

    return ResponseHotelList(rooms=rooms)

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
```

**Запрос на создание брони:**

![Screenshot_20201221_172450](https://user-images.githubusercontent.com/58785926/102786991-723ffa80-43b1-11eb-976e-d19be2b6a0f9.png)

```python
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

        isinstance(r.identifier, int) and r.identifier <= 0,

        # Нельзя зарбронировать номер раньше, чем выселиться из него
        (
                isinstance(r.date_start, date) and
                isinstance(r.date_end, date) and
                r.date_end < r.date_start
        ),
    ]):
        raise HTTPException(
            status_code=400,
            detail=HTTP_400_WRONG_PARAMS
        )

    # Бизнес-логика возвращает идентификатор созданной брони
    identifier = int(b_create(r.identifier, r.date_start, r.date_end))

    return ResponseBookingsCreate(identifier=identifier)

def bookings_create(identifier: int, date_start: date = None, date_end: date = None) -> int:
    query = f"INSERT INTO bookings (" \
            f"room_id, date_start, date_end) " \
            f"SELECT room_id, \'{date_start}\', \'{date_end}\' " \
            f"FROM hotel " \
            f"WHERE room_id = {identifier} " \
            f"RETURNING booking_id;"

    database_value = get_database_value(query)

    return database_value
```

**Запрос на удаление брони:**

![Screenshot_20201221_172634](https://user-images.githubusercontent.com/58785926/102787165-afa48800-43b1-11eb-8c5b-e87be14b0b78.png)

```python
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
    identifier = int(b_remove(r.identifier))

    return ResponseBookingsRemove(identifier=identifier)

def bookings_remove(identifier: int) -> int:
    query = f"DELETE FROM bookings WHERE booking_id = {identifier} RETURNING booking_id;"

    database_value = get_database_value(query)

    return database_value
```

**Запрос на список броней по ID комнаты:**

![Screenshot_20201221_172904](https://user-images.githubusercontent.com/58785926/102787373-09a54d80-43b2-11eb-87ce-e7510e0af1e1.png)

```python
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
    #   1. "booking_id" - идентификатор
    #   2. "date_start" - дата начала
    #   3. "date_end" - дата окончания
    # Все брони отстортированы по дате начала
    bookings = b_list(r.identifier)

    return ResponseBookingsList(bookings=bookings)

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
```
