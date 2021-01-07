import requests


class Client:
    def __init__(self):
        self.fake_api = 'https://virtual-shop.pl/api/clients'

    def add_client(self, body):
        if isinstance(body, type({'something': 'somethingelse'})) is False:
            raise TypeError('Body must be dictionary')
        if 'email' not in body or 'name' not in body or 'surname' not in body:
            raise ValueError('Body must contain email, name and surname')
        response = requests.post(self.fake_api + '/add', json=body)
        if 200 <= response.status_code <= 299:
            return response
        elif response.status_code == 409:
            return 'User of given email exists'
        else:
            return 'Some horrible error happend'

    def get_client(self, client_id):
        if type(client_id) is not int:
            raise TypeError('Client id must be integer')
        response = requests.get(self.fake_api + '/{}'.format(client_id))
        if 200 <= response.status_code <= 299:
            return response.json
        if response.status_code == 404:
            return 'User does not exist'
        else:
            return 'Something went horribly wrong'

    def get_clients(self):
        return requests.get(self.fake_api)

    def update_client(self, client_id, body):
        if type(client_id) is not int or isinstance(body, type({'s': 's'})) \
                is False:
            raise TypeError('Wrong types')
        if 'email' not in body or 'name' not in body or 'surname' not in body:
            raise ValueError('Body must contain email, name and surname')
        response = requests.put(self.fake_api + '/{}'.format(client_id), json=body)
        if 200 <= response.status_code <= 299 or response.status_code == 409 \
                or response.status_code == 404:
            return response
        else:
            return 'Something went horribly wrong'

    def delete_client(self, client_id):
        if type(client_id) is not int:
            raise TypeError('Client id must be integer')
        return requests.delete(self.fake_api + '/{}'.format(client_id))

    def get_client_orders(self, client_id):
        if type(client_id) is not int:
            raise TypeError('Client id and Order id must be integers')
        return requests.get(self.fake_api + '/{}/orders'.format(client_id))

    def get_client_order(self, client_id, order_id):
        if type(client_id) is not int or type(order_id) is not int:
            raise TypeError('Client id and Order id must be integers')
        return requests.get(self.fake_api + '/{}/order/{}'.format(
            client_id, order_id))

    def get_client_payment_amount(self, client_id):
        response = self.get_client_orders(client_id)
        amount = 0
        orders = response.json['orders']
        for order in orders:
            items = order['order']
            for item in items:
                amount += item['value']

        return amount

