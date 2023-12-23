import os
import psycopg2
from psycopg2 import sql
from utilities.log_event_handler import log_event


def delete_all_tables(host, port, database, user, password):

    connection = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )

    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            drop_table_query = sql.SQL("DROP TABLE IF EXISTS {} CASCADE").format(sql.Identifier(table_name))
            cursor.execute(drop_table_query)

        connection.commit()

        log_event.info("All tables deleted successfully.")

    except Exception as e:
        # Rollback if there's an error
        connection.rollback()
        log_event.info(f"Error: {e}")

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()


if __name__ == "__main__":
    host = os.getenv("postgresDB_HOST", None)
    database = os.getenv("postgresDB_NAME", None)
    user = os.getenv("postgresDB_USER", None)
    password = os.getenv("postgresDB_PASSWORD", None)
    port = os.getenv("postgresDB_PORT", None)

    delete_all_tables(host, port, database, user, password)
