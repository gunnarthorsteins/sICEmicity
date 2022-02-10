import os
import sys

import unittest
import sqlalchemy

# To import from other parent directory in repo
pwd = os.getcwd()
sys.path.insert(0, pwd)

import database

class DataBaseTest(unittest.TestCase):
    def test_connection(self):

    def test_writing_to_sql(self):
        

    def test_integrity(self):
        self.assertRaises(sqlalchemy.exc.IntegrityError, database.to_sql,)

    def test_incorrectly_formatted_datetime(self):

if __name__ == '__main__':
    unittest.main()