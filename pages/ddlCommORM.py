import os
from sqlalchemy import Table, Column, Integer, String, Index, MetaData, inspect, create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from utilities.log_event_handler import log_event

Base = declarative_base()


class MyTable(Base):
    __tablename__ = 'my_table'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)


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
        self.session = self._create_session()

        if inspect(self.engine).has_table('my_table'):
            Base.metadata.tables['my_table'].drop(self.engine)

    def _create_engine(self):
        log_event.info("creating db engine ...")
        return create_engine(self.db_url)

    def _create_session(self):
        log_event.info('creating session ...')
        Session = sessionmaker(bind=self.engine)
        return Session()

    def create_table_if_not_exists(self):
        log_event.info("creating my_table ...")
        if not inspect(self.engine).has_table('my_table'):
            Base.metadata.create_all(self.engine)

    def drop_table(self):
        log_event.info("Checking if the table exists...")
        if inspect(self.engine).has_table('my_table'):
            Base.metadata.tables['my_table'].drop(self.engine)
            log_event.info('table has been deleted ...')

    def add_column(self, column_name, column_type):
        if not inspect(self.engine).has_table('my_table'):
            self.create_table_if_not_exists()

        # Create the new column in the original table
        with self.engine.begin() as connection:
            connection.execute(text(f"ALTER TABLE my_table ADD COLUMN {column_name} {column_type}"))

        # Reflect the changes in the Base metadata
        Base.metadata.clear()
        Base.metadata.reflect(bind=self.engine)
        log_event.info('column has been added : ' + column_name)

    def drop_column(self, column_name):
        if inspect(self.engine).has_table('my_table'):
            table = Table('my_table', self.metadata, autoload_with=self.engine)
            column = table.columns[column_name]
            column.drop(self.engine)
            log_event.info("column has been dropped  :" + column_name)

    # def alter_column_type(self, column_name, new_column_type):
    #     if inspect(self.engine).has_table('my_table'):
    #         table = Table('my_table', self.metadata, autoload_with=self.engine)
    #         column = table.columns[column_name]
    #         column.type = new_column_type
    #         column.alter()

    def alter_column_type(self, column_name, new_column_type):
        if inspect(self.engine).has_table('my_table'):
            # Create a new temporary column with the desired type
            with self.engine.begin() as connection:
                connection.execute(text(f"ALTER TABLE my_table ADD COLUMN new_{column_name} {new_column_type}"))
                connection.execute(text(f"UPDATE my_table SET new_{column_name} = {column_name}"))
                connection.execute(
                    text(f"ALTER TABLE my_table DROP COLUMN {column_name} RENAME COLUMN new_{column_name} TO {column_name}"))

            # Reflect the changes in the Base metadata
            Base.metadata.clear()
            Base.metadata.reflect(bind=self.engine)

    def create_index(self, index_name, *columns):
        if inspect(self.engine).has_table('my_table'):
            table = Table('my_table', self.metadata, autoload_with=self.engine)
            Index(index_name, *columns).create(self.engine)
            log_event.info('index has been created at : ' + index_name)

    def drop_index(self, index_name):
        if inspect(self.engine).has_table('my_table'):
            table = Table('my_table', self.metadata, autoload_with=self.engine)
            Index(index_name).drop(self.engine)
            log_event.info('index has been dropped')

    def drop_table(self):
        Base.metadata.tables['my_table'].drop(self.engine)
        log_event.info('table : my_table has been deleted ...')
