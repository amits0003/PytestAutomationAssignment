import pytest
import psycopg2
import psycopg2.extras
import configparser


def read_config():
    config = configparser.ConfigParser()
    config.read('defaultConfig.ini')
    return config


def get_postgres_config():
    config = read_config()

    postgres_config = {
        'hostname': config.get('POSTGRES', 'HOSTNAME'),
        'database': config.get('POSTGRES', 'DATABASE'),
        'username': config.get('POSTGRES', 'USERNAME'),
        'password': config.get('POSTGRES', 'PWD'),
        'PORT': config.get('POSTGRES', 'PORT_NUM')
    }

    return postgres_config


@pytest.fixture(scope='class')
def setup(request):
    conn = None
    cur = None
    res = get_postgres_config()

    try:
        conn = psycopg2.connect(
            host=res['hostname'],
            dbname=res['database'],
            user=res['username'],
            password=res['password'],
            port=res['port']
        )
        cur = conn.cursor()
        print("Connection Successful")
        request.cls.cur = cur
        request.cls.conn = conn

    except Exception as error:
        print(error)
    yield
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
