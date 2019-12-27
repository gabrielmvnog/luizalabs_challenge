from mockupdb import MockupDB, go, OpMsg
import os
from luizalabs_project import app
import unittest
from requests.auth import _basic_auth_str
from mockupdb import bson
import json


class CutomerAPITestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.server = MockupDB(auto_ismaster=True)
        self.server.run()

        user = 'admin'
        password = 'admin'

        os.environ['MONGO_HOST'] = str(self.server.host)
        os.environ['MONGO_PORT'] = str(self.server.port)

        os.environ['API_USER'] = str(user)
        os.environ['API_PASS'] = str(password)

        self.headers = {"Authorization": _basic_auth_str(user, password),
                        'Content-Type': 'application/json'}

        app.testing = True
        self.app_test = app.test_client()

    @classmethod
    def tearDownClass(self):
        self.server.stop()

    def test_getAll(self):
        future = go(self.app_test.get,
                    '/api/customer/all', headers=self.headers)

        request = self.server.receives(
            OpMsg({"find": "customer", "filter": {}},
                  namespace="luizalabs-project")
        )
        request.ok(cursor={'id': 0, 'firstBatch': [
            {'name': 'Test_1', 'email': 'test_1@test.com'},
            {'name': 'Test_2', 'email': 'test_2@test.com'}]})

        response = future()

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Test_1", data)
        self.assertIn("Test_2", data)
        self.assertIn("test_1@test.com", data)
        self.assertIn("test_2@test.com", data)

    def test_getOne(self):
        customer_id = "5dfe806ad8bd8501a35a7039"
        future = go(self.app_test.get,
                    f'/api/customer/{customer_id}', headers=self.headers)

        request = self.server.receives(
            OpMsg({"find": "customer",
                   'filter': {'_id': bson.ObjectId(customer_id)},
                   'limit': 1,
                   'singleBatch': True},
                  namespace="luizalabs-project")
        )
        request.ok(cursor={'id': 0, 'firstBatch': [
            {'name': 'Test_1', 'email': 'test_1@test.com'}]})

        response = future()

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Test_1", data)
        self.assertNotIn("Test_2", data)
        self.assertIn("test_1@test.com", data)
        self.assertNotIn("test_2@test.com", data)

    def test_getOne_fail(self):
        customer_id = "5dfe806ad8bd8501a35a7039"
        future = go(self.app_test.get,
                    f'/api/customer/{customer_id}', headers=self.headers)

        request = self.server.receives(
            OpMsg({"find": "customer",
                   'filter': {'_id': bson.ObjectId(customer_id)},
                   'limit': 1,
                   'singleBatch': True},
                  namespace="luizalabs-project")
        )
        request.ok(cursor={'id': 0, 'firstBatch': []})

        response = future()

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, 'null\n')

    def test_addOne(self):
        name = "Test_1"
        email = "test_1@test.com"
        customer_id = "5e06802b42f0d70f613763ba"

        to_add = dict(name=name,
                      email=email)

        future = go(self.app_test.post,
                    f'/api/customer',
                    data=json.dumps(to_add),
                    headers=self.headers)

        # First check the email
        request = self.server.receives(
            {"find": "customer"})
        request.ok(cursor={'id': 0, 'firstBatch': []})

        # Add the user
        request = self.server.receives(
            {"insert": "customer"}
        )
        request.ok(cursor={'inserted_id': customer_id})

        response = future()

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Customer added with success", data)

    def test_addOne_emailExist(self):
        name = "Test_1"
        email = "test_1@test.com"

        to_add = dict(name=name,
                      email=email)

        future = go(self.app_test.post,
                    f'/api/customer',
                    data=json.dumps(to_add),
                    headers=self.headers)

        # First check the email
        request = self.server.receives(
            {"find": "customer"})
        request.ok(cursor={'id': 0, 'firstBatch': [
            {'name': 'Test_1', 'email': 'test_1@test.com'}]})

        response = future()

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Email already in use", data)

    def test_updateOne_name(self):
        to_update = dict(name="Test_3",
                         customer_id="5dfe806ad8bd8501a35a7039")

        future = go(self.app_test.put,
                    f'/api/customer',
                    data=json.dumps(to_update),
                    headers=self.headers)

        request = self.server.receives(
            OpMsg({"update": "customer"},
                  namespace="luizalabs-project")
        )
        request.ok(cursor={'id': 0, 'firstBatch': [
            {'name': 'Google', 'url': 'http://google.com/rest/api'},
            {'name': 'Rest', 'url': 'http://rest.com/rest/api'}]})

        response = future()

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Customer updated with success", data)

    def test_updateOne_email(self):
        to_update = dict(email="test_3@test.com",
                         customer_id="5dfe806ad8bd8501a35a7039")

        future = go(self.app_test.put,
                    f'/api/customer',
                    data=json.dumps(to_update),
                    headers=self.headers)

        # First check the email
        request = self.server.receives(
            {"find": "customer"})
        request.ok(cursor={'id': 0, 'firstBatch': []})

        # Update the email
        request = self.server.receives(
            OpMsg({"update": "customer"},
                  namespace="luizalabs-project")
        )
        request.ok(cursor={'id': 0, 'firstBatch': [
            {'name': 'Google', 'url': 'http://google.com/rest/api'},
            {'name': 'Rest', 'url': 'http://rest.com/rest/api'}]})

        response = future()

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Customer updated with success", data)

    def test_updateOne_emailExist(self):
        to_update = dict(email="test_3@test.com",
                         customer_id="5dfe806ad8bd8501a35a7039")

        future = go(self.app_test.put,
                    f'/api/customer',
                    data=json.dumps(to_update),
                    headers=self.headers)

        # First check the email
        request = self.server.receives(
            {"find": "customer"})
        request.ok(cursor={'id': 0, 'firstBatch': [
            {'name': 'Test_3', 'email': 'test_3@test.com'}]})

        response = future()

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Couldn't update the user, email already in use", data)

    def test_updateOne_none(self):
        to_update = dict(customer_id="5dfe806ad8bd8501a35a7039")

        future = go(self.app_test.put,
                    f'/api/customer',
                    data=json.dumps(to_update),
                    headers=self.headers)

        response = future()

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Please, update need name or email as parameters", data)

    def test_deleteOne(self):
        to_delete = dict(customer_id="5dfe806ad8bd8501a35a7039")

        future = go(self.app_test.delete,
                    f'/api/customer',
                    data=json.dumps(to_delete),
                    headers=self.headers)

        request = self.server.receives(
            OpMsg({"delete": "customer"},
                  namespace="luizalabs-project")
        )
        request.ok({'acknowledged': True, 'n': 1})

        response = future()

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Customer removed with success", data)

    def test_deleteOne_fail(self):
        to_delete = dict(customer_id="5dfe806ad8bd8501a35a7039")

        future = go(self.app_test.delete,
                    f'/api/customer',
                    data=json.dumps(to_delete),
                    headers=self.headers)

        request = self.server.receives(
            OpMsg({"delete": "customer"},
                  namespace="luizalabs-project")
        )
        request.ok({'acknowledged': True, 'n': 0})

        response = future()

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Couldn't remove the user", data)


if __name__ == '__main__':
    unittest.main()
