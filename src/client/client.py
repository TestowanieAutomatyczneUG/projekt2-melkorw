import requests


class Client:
    def __init__(self):
        self.api = 'https://virtual-shop.pl/api'

    def add_client(self, body):
        if isinstance(body, type({'something': 'somethingelse'})) is False:
            raise TypeError('Body must be dictionary')
        if 'email' not in body:
            raise ValueError('Body must contain email, name and surname')
        response = requests.post(self.api+'/add', json=body)
        if 200 <= response.status_code <= 299:
            return response
        elif response.status_code == 409:
            return 'User of given email exists'
        else:
            return 'Some horrible error happend'

    def get_client(self, client_id):
        pass

    def get_clients(self):
        pass

    def update_client(self, client_id, body):
        pass
