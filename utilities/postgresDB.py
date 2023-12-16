import os
from sqlalchemy import create_engine, MetaData


class PostgresDBSetup:
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
