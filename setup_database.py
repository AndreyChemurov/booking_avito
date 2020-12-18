import psycopg2
from settings import connection_params


def create_tables() -> bool:
    # Все должно быть в файле settings, значения берутся из env, а env формируется в докере
    # connection = psycopg2.connect(**connection_params)
    # connection_params в файле settings (словарь)

    connection = None

    try:
        connection = psycopg2.connect(**connection_params)
        cursor = connection.cursor()
        cursor.execute('SELECT')
        cursor.close()
    except psycopg2.DatabaseError as e:
        print(e)
        raise e
    finally:
        if connection is not None:
            connection.close()


def drop_tables():
    pass
