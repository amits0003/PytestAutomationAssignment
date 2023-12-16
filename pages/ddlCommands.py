import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, inspect, text, select

from utilities.log_event_handler import log_event


class DDLCommands:

    def __init__(self):
        self.db_config = {
            'host': os.getenv("postgresDB_HOST", None),
            'database': os.getenv("postgresDB_NAME", None),
            'user': os.getenv("postgresDB_USER", None),
            'password': os.getenv("postgresDB_PASSWORD", None),
            'port': os.getenv("postgresDB_PORT", None)
        }

        self.db_url = (f"postgresql://{self.db_config['user']}:{self.db_config['password']}@{self.db_config['host']}:"
                       f"{self.db_config['port']}/{self.db_config['database']}")
        self.engine = self._create_engine()
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)

    def _create_engine(self):
        return create_engine(self.db_url)

    def create_table(self, table_name, column_data):
        """
        # Define the table column
            columns = [ Column('id', Integer, primary_key=True),
                        Column('name', String),
                        Column('age', Integer)
                      ]
        # use the Table name as given in the PostgresDBSetup : for example : Employee
        """

        tableX = Table(table_name, self.metadata, *column_data, extend_existing=True)
        # Check if the table already exists
        inspector = inspect(self.engine)
        if table_name not in inspector.get_table_names():
            # If not, create the table
            tableX.create(self.engine, checkfirst=True)
            log_event.info(table_name + " : creation successful")
        else:
            log_event.info(table_name + " : already exists")

        return tableX

    def read_all_data_from_table(self, table_name):

        # Choose a table to query (replace 'your_table' with the actual table name)
        tableObj = Table(table_name, self.metadata, autoload_with=self.engine)

        # Create a connection to the database
        with self.engine.connect() as connection:
            query = tableObj.select()
            result = connection.execute(query)

            rows = result.fetchall()

            try:
                json_data = [row for row in rows]
            except Exception as e:
                log_event.error("Error converting rows to dictionary:", e)
                json_data = None

        return json_data

    def add_columns_into_table(self, table_name, column_name, column_type):
        tableObj = Table(table_name, self.metadata)
        column = Column(column_name, column_type)
        tableObj.append_column(column, replace_existing=True)
        tableObj.create(self.engine)
        log_event.info("columns has been added")

    def drop_column_from_table(self, table_name, column_to_delete):
        table = Table(table_name, self.metadata)
        # Check if the column exists before proceeding
        if column_to_delete in table.columns:
            # Create a new table without the specified column
            new_columns = [c for c in table.columns if c.name != column_to_delete]
            new_table = Table(table_name + '_new', self.metadata, *new_columns)
            new_table.create(self.engine)

            self.drop_table_from_db(table_name)

            # Rename the new table to the original table name
            with self.engine.connect() as connection:
                sql_statement = text(f'ALTER TABLE {table_name}_new RENAME TO {table_name}')
                connection.execute(sql_statement)

        else:
            log_event.info(f"Column '{column_to_delete}' does not exist in the table '{table_name}'")

    def drop_table_from_db(self, table_name):
        table = Table(table_name, self.metadata)
        table.drop(self.engine, checkfirst=True)
        log_event.info(f"Table '{table_name}' has been deleted.")
