from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect
import os

Base = declarative_base()


class MyTable(Base):
    __tablename__ = 'my_table'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)


class DMLCommands:

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
        return create_engine(self.db_url)

    def _create_session(self):
        Session = sessionmaker(bind=self.engine)
        return Session()

    def create_table_if_not_exists(self):
        if not inspect(self.engine).has_table('my_table'):
            Base.metadata.create_all(self.engine)

    def insert_data(self, name, age):
        new_data = MyTable(name=name, age=age)
        self.session.add(new_data)
        self.session.commit()

    def update_data(self, record_id, new_name, new_age):
        record = self.session.query(MyTable).get(record_id)
        if record:
            record.name = new_name
            record.age = new_age
            self.session.commit()

    def delete_data(self, record_id):
        record = self.session.query(MyTable).get(record_id)
        if record:
            self.session.delete(record)
            self.session.commit()

    def query_data(self):
        return self.session.query(MyTable).all()

    def drop_table(self):
        Base.metadata.tables['my_table'].drop(self.engine)
