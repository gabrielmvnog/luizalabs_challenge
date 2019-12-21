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
            self.collection.insert_one(dict(name=name, email=email))

            return True

        return None

    def update(self, object_id, name, email):

        if name and email:
            if self.__check_email(email):
                return False

            self.collection.update_one({'_id': ObjectId(object_id)},
                                       {'$set': {
                                        'name': name,
                                        'email': email
                                        }}, upsert=False)
        elif name:
            self.collection.update_one({'_id': ObjectId(object_id)},
                                       {'$set': {
                                           'name': name
                                       }})
        elif email:

            if self.__check_email(email):
                return False

            self.collection.update_one({'_id': ObjectId(object_id)},
                                       {'$set': {
                                           'email': name
                                       }})

        return True

    def show_all(self):

        return list(self.collection.find({}))

    def remove(self, object_id):

        result = self.collection.remove(dict(_id=ObjectId(object_id)))

        if result['n']:
            return True

        return None
