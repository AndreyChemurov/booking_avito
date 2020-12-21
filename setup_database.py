import psycopg2
from settings import connection_params


def create_tables():
    """ Создание таблиц. Если таблицы созданы, то меняет конфиг,
     который проверяется при каждом новом запуске прилоежния.
     """

    connection, cursor = None, None

    try:
        connection = psycopg2.connect(**connection_params)
        cursor = connection.cursor()

        sql_create_tables_query = """
        CREATE TABLE IF NOT EXISTS "hotel" (
            room_id SERIAL PRIMARY KEY NOT NULL,
            description TEXT NOT NULL,
            price INTEGER NOT NULL,
            created_at DATE NOT NULL DEFAULT CURRENT_DATE
        );
        
        CREATE TABLE IF NOT EXISTS "bookings" (
            booking_id BIGSERIAL PRIMARY KEY NOT NULL,
            room_id INTEGER NOT NULL,
            date_start DATE NOT NULL,
            date_end DATE NOT NULL
        );
        
        CREATE UNIQUE INDEX h_room_idx ON hotel (room_id);
        CREATE INDEX h_price_idx ON hotel (price);
        CREATE INDEX h_created_at_idx ON hotel (created_at);
        
        CREATE UNIQUE INDEX b_id_idx ON bookings (booking_id);
        CREATE INDEX b_room_idx ON bookings (room_id);
        CREATE INDEX b_date_start_idx ON bookings (date_start);
        """

        cursor.execute(sql_create_tables_query)
        connection.commit()

        cursor.close()
    except psycopg2.DatabaseError as e:
        print(e)
        return False
    finally:
        if not connection.closed:
            connection.close()
        if not cursor.closed:
            cursor.close()

    return True
