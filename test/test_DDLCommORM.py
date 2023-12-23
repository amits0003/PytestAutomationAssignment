import os
import sys

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

import unittest
from unittest.mock import patch
from sqlalchemy import create_engine, inspect, Integer, String
from base.BaseTest import BaseTest
from pages.ddlCommORM import DDLCommands, Base, MyTable
from utilities.log_event_handler import log_event


class TestDDLCommands(BaseTest):

    def setUp(self):
        log_event.info("Setup Starting ...")
        self.ddl_commands = DDLCommands()
        self.ddl_commands.create_table_if_not_exists()
        self.transaction = self.ddl_commands.session.begin()

    def tearDown(self):
        self.ddl_commands.session.rollback()
        log_event.info("Teardown Successful")

    def test_create_table_if_not_exists(self):
        self.ddl_commands.create_table_if_not_exists()
        inspector = inspect(self.ddl_commands.engine)
        # Assert that the table exists in the database
        self.assertTrue(inspector.has_table('my_table'))
        self.log_test_result()

    def test_drop_table(self):
        self.ddl_commands.create_table_if_not_exists()
        self.ddl_commands.drop_table()
        inspector = inspect(self.ddl_commands.engine)
        # Assert that the table is dropped (not existing) in the database
        self.assertFalse(inspector.has_table('my_table'))
        self.log_test_result()

    def test_create_index(self):
        self.ddl_commands.create_table_if_not_exists()
        self.ddl_commands.create_index('idx_name', MyTable.name)
        inspector = inspect(self.ddl_commands.engine)
        # Assert that the index is created on the specified column
        indexes = inspector.get_indexes('my_table')
        index_names = [index['name'] for index in indexes]
        self.assertIn('idx_name', index_names)
        self.log_test_result()


if __name__ == '__main__':
    unittest.main()
