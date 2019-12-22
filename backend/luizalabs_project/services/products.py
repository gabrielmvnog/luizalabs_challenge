import requests

class MagaluProducts():

    @staticmethod
    def list_products(page_n):
        url_list = f'http://challenge-api.luizalabs.com/api/product/?page={page_n}'

        req = requests.get(url_list)

    @staticmethod
    def check_product(prod_id):
        url_detail = f'http://challenge-api.luizalabs.com/api/product/{prod_id}'

        req = requests.get(url_detail)
        if req.status_code == 200:
            return req.json()

        return None
