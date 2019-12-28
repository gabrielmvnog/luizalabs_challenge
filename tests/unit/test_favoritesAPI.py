from mockupdb import MockupDB, go, OpMsg
import os
from luizalabs_project import app
import unittest
from requests.auth import _basic_auth_str
from mockupdb import bson
import json


class FavoritesAPITestCase(unittest.TestCase):

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

    def test_getFavorites(self):
        customer_id = "5dfe806ad8bd8501a35a7039"
        future = go(self.app_test.get,
                    f'/api/favorites/{customer_id}', headers=self.headers)

        request = self.server.receives(
            OpMsg({"find": "customer",
                   'filter': {'_id': bson.ObjectId(customer_id)},
                   'limit': 1,
                   'singleBatch': True},
                  namespace="luizalabs-project")
        )
        request.ok(cursor={'id': 0, 'firstBatch': [
            {'name': 'Test_1', 'fav_products': []}]})

        response = future()

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('[]', data)

    def test_addFavorite(self):
        customer_id = "5e06802b42f0d70f613763ba"
        product_id = "1bf0f365-fbdd-4e21-9786-da459d78dd1f"

        to_add = dict(customer_id=customer_id,
                      product_id=product_id)

        future = go(self.app_test.post,
                    f'/api/favorite',
                    data=json.dumps(to_add),
                    headers=self.headers)

        # Check Favorite list
        request = self.server.receives(
            OpMsg({"find": "customer"})
        )
        request.ok(cursor={'id': 0, 'firstBatch': [{'fav_products': []}]})

        # Insert item in favorite list
        request = self.server.receives(
            OpMsg({"update": "customer"})
        )
        request.ok()

        response = future()

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("insertion with success", data)

    def test_addFavorite_fail(self):
        customer_id = "5e06802b42f0d70f613763ba"
        product_id = "1bf0f365-fbdd-4e21-9786-da459d78dd1f"

        to_add = dict(customer_id=customer_id,
                      product_id=product_id)

        future = go(self.app_test.post,
                    f'/api/favorite',
                    data=json.dumps(to_add),
                    headers=self.headers)

        # Check Favorite list
        request = self.server.receives(
            OpMsg({"find": "customer"})
        )
        request.ok(cursor={'id': 0,
                           'firstBatch': [{'fav_products': [product_id]}]})

        response = future()

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("item duplicated", data)

    def test_deleteFavorite(self):
        customer_id = "5e06802b42f0d70f613763ba"
        product_id = "1bf0f365-fbdd-4e21-9786-da459d78dd1f"

        to_delete = dict(customer_id=customer_id,
                         product_id=product_id)

        future = go(self.app_test.delete,
                    f'/api/favorite',
                    data=json.dumps(to_delete),
                    headers=self.headers)

        # Check Favorite list
        request = self.server.receives(
            OpMsg({"find": "customer"})
        )
        request.ok(cursor={'id': 0,
                           'firstBatch': [{'fav_products': [product_id]}]})

        # Delete item from favorite list
        request = self.server.receives(
            OpMsg({"update": "customer"})
        )
        request.ok()

        response = future()

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("removed with success", data)

    def test_deleteFavorite_fail(self):
        customer_id = "5e06802b42f0d70f613763ba"
        product_id = "1bf0f365-fbdd-4e21-9786-da459d78dd1f"

        to_delete = dict(customer_id=customer_id,
                         product_id=product_id)

        future = go(self.app_test.delete,
                    f'/api/favorite',
                    data=json.dumps(to_delete),
                    headers=self.headers)

        # Check Favorite list
        request = self.server.receives(
            OpMsg({"find": "customer"})
        )
        request.ok(cursor={'id': 0,
                           'firstBatch': [{'fav_products': []}]})

        response = future()

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("item not found", data)


if __name__ == '__main__':
    unittest.main()
