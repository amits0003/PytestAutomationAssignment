import os
import sys

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

import unittest
from sqlalchemy import func
from base.BaseTest import BaseTest
from pages.dmlCommORM import DMLCommands
from utilities.log_event_handler import log_event


class TestDMLCommands(BaseTest):

    def setUp(self):
        log_event.info("Setup Starting ...")
        self.dml_commands = DMLCommands()
        self.dml_commands.create_table_if_not_exists()
        self.transaction = self.dml_commands.session.begin()

    def tearDown(self):
        self.dml_commands.session.rollback()
        log_event.info("Teardown Successful")

    def test_insert_data(self):
        # self.dml_commands.create_table_if_not_exists()
        self.dml_commands.insert_data('Amit Kumar', 25)
        result = self.dml_commands.query_data()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, 'Amit Kumar')
        self.assertEqual(result[0].age, 25)
        self.log_test_result()

    def test_update_data(self):
        # self.dml_commands.create_table_if_not_exists()
        self.dml_commands.insert_data('Sumit Kumar', 25)
        record_id = self.dml_commands.query_data()[0].id

        self.dml_commands.update_data(record_id, 'Sumit Kumar', 30)
        result = self.dml_commands.query_data()
        self.assertEqual(result[0].name, 'Sumit Kumar')
        self.assertEqual(result[0].age, 30)
        self.log_test_result()

    def test_delete_data(self):
        # self.dml_commands.create_table_if_not_exists()
        self.dml_commands.insert_data('Ramesh Kumar', 25)
        record_id = self.dml_commands.query_data()[0].id

        self.dml_commands.delete_data(record_id)
        result = self.dml_commands.query_data()
        self.assertEqual(len(result), 0)
        self.log_test_result()

    def test_query_data(self):
        # self.dml_commands.create_table_if_not_exists()
        self.dml_commands.insert_data('Steve Jackson', 25)
        result = self.dml_commands.query_data()
        self.assertTrue(result)
        # self.dml_commands.drop_table()
        self.log_test_result()


if __name__ == '__main__':
    unittest.main()
