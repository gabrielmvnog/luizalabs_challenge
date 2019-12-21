import requests

class MagaluProducts():

    @staticmethod
    def list_products(page_n):
        url_list = f'http://challenge-api.luizalabs.com/api/product/?page={page_n}'

        req = requests.get(url_list)

        print(req.json())

    @staticmethod
    def detail_product(prod_id):
        url_detail = f'http://challenge-api.luizalabs.com/api/product/{prod_id}'

        req = requests.get(url_detail)

        print(req.json())


MagaluProducts.detail_product('69e2f68f-20cc-b9c0-8365-89928a2dcf88')
