from pymongo import MongoClient
from bson import ObjectId


class Database():
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.database = self.client['luizalabs-project']

    def __del__(self):
        self.client.close()


class CustomerDB(Database):

    def __init__(self):
        super().__init__()
        self.collection = self.database.customer

    def __check_email(self, email):
        result = self.collection.find_one({"email": email})

        return result

    def add(self, name, email):

        if not self.__check_email(email):
            self.collection.insert_one(
                dict(name=name, email=email, fav_products=list()))

            return True

        return None

    def update(self, customer_id, name, email):

        if name and email:
            if self.__check_email(email):
                return False

            self.collection.update_one({'_id': ObjectId(customer_id)},
                                       {'$set': {
                                        'name': name,
                                        'email': email
                                        }}, upsert=False)
        elif name:
            self.collection.update_one({'_id': ObjectId(customer_id)},
                                       {'$set': {
                                           'name': name
                                       }})
        elif email:

            if self.__check_email(email):
                return False

            self.collection.update_one({'_id': ObjectId(customer_id)},
                                       {'$set': {
                                           'email': name
                                       }})

        return True

    def show_all(self):

        return list(self.collection.find({}))

    def show_one(self, customer_id):

        return self.collection.find_one({'_id': ObjectId(customer_id)})

    def remove(self, customer_id):

        result = self.collection.remove(dict(_id=ObjectId(customer_id)))

        if result['n']:
            return True

        return None

    def get_favorites(self, customer_id):

        favorites = self.collection.find_one({'_id': ObjectId(customer_id)},
                                             {'fav_products': 1})['fav_products']

        return favorites

    def insert_favorite(self, customer_id, product_id):

        favorites = self.get_favorites(customer_id)

        if product_id not in favorites:
            self.collection.update_one({'_id': ObjectId(customer_id)},
                                       {'$addToSet': {
                                           'fav_products': product_id
                                       }})

            return True

        return None

    def remove_favorite(self, customer_id, product_id):

        self.collection.update_one({'_id': ObjectId(customer_id)},
                                    {'$pull': {
                                        'fav_products': product_id
                                    }})