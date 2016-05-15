import unittest
from unittest import TestCase
import server
from server import app

# make tests fail to make sure they can fail

###############################################

# TESTING FLASK

class FlaskTest(TestCase):

    def setup(self):
        """To do before every test"""

        self.client = app.test_cliet()
        app.config['TESTING'] = True

    def test_flask_route(self):
        """test route (404)/ test html"""

        result = self.client.get("/my-route")


        ### CHECK OUT http://flask.pocoo.org/docs/0.10/testing


# TESTING DB

# use temporary db. with sample data

def setUp(self):
    """Do before every test"""

    # Connect to test db
    connect_to_dn(app, "postgresql://testdb")

    #Create tables and add sample data
    db.create_all()
    example_data()

def tearDown(self):
    """Do after every test"""

    db.session.close()
    db.drop_all()

def test_db_thing(self):


def _mock_(arg):
    return smth _mock_

????



class MyAppUnitTestCase(unittest.TestCase):

    def test
