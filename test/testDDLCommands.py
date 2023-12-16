import unittest
import random
from sqlalchemy import inspect, Table, Column, Integer, String
from base.BaseTest import BaseTest
from pages.ddlCommands import DDLCommands
from utilities.log_event_handler import log_event


class TestDDLCommands(BaseTest):

    def setUp(self):
        log_event.info("Setup Starting ...")
        self.ddl_commands = DDLCommands()

    def tearDown(self):
        # Clean up: Drop the 'BookShelf' table if it exists
        inspector = inspect(self.ddl_commands.engine)
        if 'BookShelf' in inspector.get_table_names():
            self.ddl_commands.drop_table_from_db('BookShelf')
        log_event.info("Teardown Successful")

    def test_create_table(self):
        # Define columns for the BookShelf table
        columns = [
            Column('ID', Integer, primary_key=True),
            Column('bookName', String),
            Column('price', Integer),
            Column('subject', String)
        ]

        # Drop the 'BookShelf' table if it already exists
        inspector = inspect(self.ddl_commands.engine)
        if 'BookShelf' in inspector.get_table_names():
            self.ddl_commands.drop_table_from_db('BookShelf')
            log_event.info("BookSelf table has been found existing and is deleted")

        # Test create_table function
        self.ddl_commands.create_table('BookShelf', columns)

        # Verify that the table has been created
        inspector = inspect(self.ddl_commands.engine)
        self.assertTrue('BookShelf' in inspector.get_table_names())
        self.log_test_result()

    def test_read_all_data_from_table(self):

        inspector = inspect(self.ddl_commands.engine)
        if 'BookShelf' not in inspector.get_table_names():
            self.test_create_table()

        data = self.ddl_commands.read_all_data_from_table('BookShelf')
        log_event.info("data from table : " + str(data))

        # Verify that data is not None
        self.assertIsNotNone(data)
        self.log_test_result()

    def test_add_columns_into_table(self):
        random_integer = random.randint(1, 100)
        table_name = 'book_' + str(random_integer)
        log_event.info("table created : " + table_name)
        self.ddl_commands.add_columns_into_table(table_name, 'test_col', String)

        # Verify that the new column has been added
        inspector = inspect(self.ddl_commands.engine)
        columns = [column['name'] for column in inspector.get_columns(table_name)]
        self.assertTrue('test_col' in columns)
        self.log_test_result()

    def test_drop_table_from_db(self):
        # Assuming 'BookShelf' table has been created, test drop_table_from_db function
        self.ddl_commands.drop_table_from_db('BookShelf')

        # Verify that the 'BookShelf' table has been dropped
        inspector = inspect(self.ddl_commands.engine)
        self.assertFalse('BookShelf' in inspector.get_table_names())
        self.log_test_result()


if __name__ == '__main__':
    unittest.main()
