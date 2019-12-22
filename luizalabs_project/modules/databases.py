from pymongo import MongoClient
from bson import ObjectId

from luizalabs_project.config import MONGO_HOST, MONGO_PORT

class Database():
    def __init__(self):
        self.client = MongoClient(MONGO_HOST, int(MONGO_PORT))
        self.database = self.client['luizalabs-project']

    def __del__(self):
        self.client.close()


class CustomerDB(Database):

    def __init__(self):
        super().__init__()
        self.collection = self.database.customer

    def __check_email(self, email: str):
        """
        Check if email already exist.
    
        PARAMETERS
        ----------
            - email: string to be searched.
        """

        result = self.collection.find_one({"email": email})

        return result

    def add(self, name: str, email: str) -> bool:
        """
        add a new customer to database.
    
        PARAMETERS
        ----------
            - name: string representing a name.
            - email: string that must be unique in the database.
        RETURN:
        -------
            - A boolean representing success or failure. 
        """

        if not self.__check_email(email):
            self.collection.insert_one(
                dict(name=name, email=email, fav_products=list()))

            return True

        return None

    def update(self, customer_id: str, name: str, email: str) -> bool:
        """
        update an existing customer in database.
    
        PARAMETERS
        ----------
            - customer_id: an unique ID that represent the customer
                to be updated.
            - name: string representing a name. (can be none)
            - email: string representing the email. (can be none)
        RETURN:
        -------
            - A boolean representing success or failure. 
        """

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

    def show_all(self) -> list:
        """
        show all customers from the database.

        RETURN:
        -------
            - A list of costumers. 
        """

        return list(self.collection.find({}))

    def show_one(self, customer_id) -> dict:
        """
        show one customer from the database.
    
        PARAMETERS
        ----------
            - customer_id: an unique ID that represent the customer
                to be searched.
        RETURN:
        -------
            - Informations about one customer. 
        """

        return self.collection.find_one({'_id': ObjectId(customer_id)})

    def remove(self, customer_id: str) -> bool:
        """
        remove an existing customer in database.
    
        PARAMETERS
        ----------
            - customer_id: an unique ID that represent the customer
                to be searched.
        RETURN:
        -------
            - A boolean representing success or failure. 
        """

        result = self.collection.remove(dict(_id=ObjectId(customer_id)))

        if result['n']:
            return True

        return None

    def get_favorites(self, customer_id: str) -> dict:
        """
        show one customer's favorite products from the database.
    
        PARAMETERS
        ----------
            - customer_id: an unique ID that represent the customer
                to be searched.
        RETURN:
        -------
            - Informations about the products of the customer. 
        """

        favorites = self.collection.find_one({'_id': ObjectId(customer_id)},
                                             {'fav_products': 1})['fav_products']

        return favorites

    def insert_favorite(self, customer_id: str, product_id: str) -> bool:
        """
        insert one customer's favorite products in database.
    
        PARAMETERS
        ----------
            - customer_id: an unique ID that represent the customer
                to be searched.
            - product_id: an unique ID that represent the product
                to be added.
        RETURN:
        -------
            - A boolean representing success or failure. 
        """

        favorites = self.get_favorites(customer_id)

        if product_id not in favorites:
            self.collection.update_one({'_id': ObjectId(customer_id)},
                                       {'$addToSet': {
                                           'fav_products': product_id
                                       }})

            return True

        return None

    def remove_favorite(self, customer_id: str, product_id: str) -> bool:
        """
        remove one customer's favorite products in database.
    
        PARAMETERS
        ----------
            - customer_id: an unique ID that represent the customer
                to be searched.
            - product_id: an unique ID that represent the product
                to be removed.
        RETURN:
        -------
            - A boolean representing success or failure. 
        """

        favorites = self.get_favorites(customer_id)

        if product_id in favorites:

            self.collection.update_one({'_id': ObjectId(customer_id)},
                                                {'$pull': {
                                                    'fav_products': product_id
                                                }})

            return True

        return None
