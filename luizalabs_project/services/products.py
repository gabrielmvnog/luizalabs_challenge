import requests

class MagaluProducts():
    """ An helper class to get the list of products and check on value """

    @staticmethod
    def list_products(page_n: str):
        """
        Get the list of products in the Magalu API.
    
        PARAMETERS
        ----------
            - page_n: string of the page number.
        RETURNS
        -------
            - A json with the list of product in Magalu API.
        """

        url_list = f'http://challenge-api.luizalabs.com/api/product/?page={page_n}'
        req = requests.get(url_list)        

        if req.status_code == 200:
            return req.json()

        return None

    @staticmethod
    def check_product(prod_id: str):
        """
        Check a product in the Magalu API.
    
        PARAMETERS
        ----------
            - prod_id: string of the product id.
        RETURNS
        -------
            - A json with the informations about the product.
        """

        url_detail = f'http://challenge-api.luizalabs.com/api/product/{prod_id}'

        req = requests.get(url_detail)
        if req.status_code == 200:
            return req.json()

        return None
