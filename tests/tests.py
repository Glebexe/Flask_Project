import unittest
from flask import current_app
from app import create_app, db


class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def test_app_exit(self):
        self.assertFalse(current_app is None)

    def test_app_isTesting(self):
        self.assertTrue(current_app.config['TESTING'])
