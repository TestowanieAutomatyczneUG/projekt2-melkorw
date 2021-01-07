import unittest
from assertpy import *
from unittest.mock import *
from client.client import Client


def create_request_mock(to_mock, fake_response):
    to_mock.return_value = Mock(ok=True)
    to_mock.return_value = fake_response


class ClientTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = Client()

    @patch('src.client.client.requests.post')
    def test_add_client(self, mock_post):
        create_request_mock(mock_post, FakeResponse(201, {'id': 1}))
        response = self.temp.add_client({'name': 'Olek', 'surname': 'Wardyn', 'email': 'olekwardyn@gmail.com'})
        assert_that(response.json['id']).is_greater_than(0)

    @patch('src.client.client.requests.post')
    def test_add_client_mock_post_called(self, mock_post):
        create_request_mock(mock_post, FakeResponse(201, {'id': 1}))
        self.temp.add_client({'name': 'Olek', 'surname': 'Wardyn', 'email': 'olekwardyn@gmail.com'})
        mock_post.assert_called_once()

    def test_add_client_type_error(self):
        assert_that(self.temp.add_client).raises(
            TypeError).when_called_with('string')

    def test_add_client_value_error_missing_field(self):
        # assert with json with missing field email
        assert_that(self.temp.add_client).raises(
            ValueError).when_called_with({'name': 'Olek', 'surname': 'Wardyn'})

    @patch('src.client.client.requests.post')
    def test_add_client_existing_email(self, mock_post):
        create_request_mock(mock_post, FakeResponse(409))
        response = self.temp.add_client({'name': 'Olek', 'surname':
            'Wardyn', 'email': 'olekwardyn@gmail.com'})
        assert_that(response).is_equal_to('User of given email exists')

    @patch('src.client.client.requests.post')
    def test_add_client_other_errors_mock_called(self, mock_post):
        create_request_mock(mock_post, FakeResponse(404,
                                                    error_message='Mock has been called'))
        self.temp.add_client({'name': 'Olek', 'surname': 'Wardyn', 'email': 'olekwardyn@gmail.com'})
        mock_post.assert_called_once()

    def test_get_client_with_id(self):
        client_id = 1
        self.temp.get_client = Mock()
        self.temp.get_client.return_value = {'name': 'Olek', 'surname': 'Wardyn',
                                             'email':
                                                 'olekwardyn@gmail.com',
                                             'id': client_id}
        response = self.temp.get_client(client_id)
        self.assertEqual(response['email'], 'olekwardyn@gmail.com')

    def test_get_client_with_id_mock_called(self):
        self.temp.get_client = Mock()
        self.temp.get_client.return_value = {'name': 'Olek',
                                             'surname':
                                                 'Wardyn',
                                             'email':
                                                 'olekwardyn@gmail.com',
                                             'id': 1}
        self.temp.get_client(1)
        self.temp.get_client.assert_called_with(1)

    @patch('src.client.client.requests.get')
    def test_get_client_not_existing_client(self, mock_get):
        create_request_mock(mock_get, FakeResponse(404))
        response = self.temp.get_client(2)
        self.assertEqual(response, 'User does not exist')

    @patch('src.client.client.requests.get')
    def test_get_client_not_existing_client_mock_called(self, mock_get):
        create_request_mock(mock_get, FakeResponse(404))
        self.temp.get_client(2)
        mock_get.assert_called_once()

    @patch('src.client.client.requests.get')
    def test_get_client_error(self, mock_get):
        create_request_mock(mock_get, FakeResponse(400))
        response = self.temp.get_client(3)
        self.assertEqual(response, 'Something went horribly wrong')

    @patch('src.client.client.requests.get')
    def test_get_client_error_mock_called(self, mock_get):
        create_request_mock(mock_get, FakeResponse(400))
        self.temp.get_client(3)
        mock_get.assert_called_once()

    def test_get_client_id_type_error(self):
        assert_that(self.temp.get_client).raises(
            TypeError).when_called_with('id')

    def test_get_client_internet_error(self):
        self.temp.get_client = Mock(side_effect=ConnectionError('Error'))
        assert_that(self.temp.get_client).raises(
            ConnectionError).when_called_with(1)

    def test_get_clients(self):
        self.temp.get_clients = Mock()
        self.temp.get_clients.return_value = FakeResponse(200,
                                                          {'results': [{'name':
                                                                            'Olek',
                                                                        'surname':
                                                                            'Wardyn',
                                                                        'email':
                                                                            'olekwardyn@gmail.com',
                                                                        'id': 1},
                                                                       {'name':
                                                                            'Andrzej',
                                                                        'surname':
                                                                            'Czarodziej',
                                                                        'email':
                                                                            'example@gmail.com',
                                                                        'id': 2}]})
        response = self.temp.get_clients()
        self.assertEqual(len(response.json['results']), 2)

    def test_get_clients_mock_called(self):
        self.temp.get_clients = MagicMock()
        self.temp.get_clients.return_value = FakeResponse(200,
                                                          {'results': [{'name':
                                                                            'Olek',
                                                                        'surname':
                                                                            'Wardyn',
                                                                        'email':
                                                                            'olekwardyn@gmail.com',
                                                                        'id': 1},
                                                                       {'name':
                                                                            'Andrzej',
                                                                        'surname':
                                                                            'Czarodziej',
                                                                        'email':
                                                                            'example@gmail.com',
                                                                        'id': 2}]})
        self.temp.get_clients()
        self.temp.get_clients.assert_called_once()

    def test_get_clients_connection_error(self):
        self.temp.get_clients = Mock(side_effect=ConnectionError('Error'))
        assert_that(self.temp.get_clients).raises(ConnectionError)

    @patch('src.client.client.requests.put')
    def test_update_client(self, mock_put):
        client_id = 1
        create_request_mock(mock_put, FakeResponse(200, {'id': client_id}))
        response = self.temp.update_client(client_id, {'name': 'Olek',
                                                       'surname':
                                                           'Wardyn2',
                                                       'email': 'olekwardyn@gmail.com'})
        assert_that(response.json['id']).is_equal_to(client_id)

    @patch('src.client.client.requests.put')
    def test_update_client_mock_called(self, mock_put):
        create_request_mock(mock_put, FakeResponse(200, {'id': 1}))
        self.temp.update_client(1, {'name': 'Olek',
                                    'surname':
                                        'Wardyn2',
                                    'email': 'olekwardyn@gmail.com'})
        mock_put.assert_called_once()

    def test_update_client_type_error(self):
        assert_that(self.temp.update_client).raises(
            TypeError).when_called_with('integer', {'name': 'Olek'})

    def test_update_client_type_error_2(self):
        assert_that(self.temp.update_client).raises(
            TypeError).when_called_with(2, 'object')

    def test_update_client_value_error_missing_field(self):
        # assert with json with missing field email
        assert_that(self.temp.update_client).raises(
            ValueError).when_called_with(2, {'name': 'Olek', 'surname': 'Wardyn'})

    def test_update_client_existing_email(self):
        self.temp.update_client = Mock()
        self.temp.update_client.return_value = FakeResponse(409,
                                                            error_message='Email already exists')
        response = self.temp.update_client(1, {'name': 'Olek', 'surname':
            'Wardyn', 'email': 'olekwardyn@gmail.com'})
        assert_that(response.error_message).is_equal_to('Email already exists')

    def test_update_client_existing_email_mock_called(self):
        self.temp.update_client = Mock()
        self.temp.update_client.return_value = FakeResponse(409,
                                                            error_message='Email already exists')
        self.temp.update_client(1, {'name': 'Olek', 'surname':
            'Wardyn', 'email': 'olekwardyn@gmail.com'})
        self.temp.update_client.assert_called_once()

    @patch('src.client.client.requests.put')
    def test_update_client_user_does_not_exist(self, mock_put):
        create_request_mock(mock_put, FakeResponse(404,
                                                   error_message='User does not exist'))
        response = self.temp.update_client(3, {'name': 'Olek', 'surname':
            'Wardyn', 'email': 'olekwardyn@gmail.com'})
        assert_that(response.error_message).contains('does', 'not')

    @patch('src.client.client.requests.put')
    def test_update_client_user_does_not_exist_mock_called(self, mock_put):
        create_request_mock(mock_put, FakeResponse(404,
                                                   error_message='User does not exist'))
        self.temp.update_client(3, {'name': 'Olek', 'surname':
            'Wardyn', 'email': 'olekwardyn@gmail.com'})
        mock_put.assert_called_once()

    @patch('src.client.client.requests.put')
    def test_update_client_other_errors(self, mock_put):
        create_request_mock(mock_put, FakeResponse(403))
        response = self.temp.update_client(1, {'name': 'Olek', 'surname':
            'Wardyn', 'email': 'olekwardyn@gmail.com'})
        assert_that(response).is_equal_to_ignoring_case('SOMETHING WENT '
                                                        'HORRIBLY WRONG')

    @patch('src.client.client.requests.put')
    def test_update_client_other_errors_mock_called(self, mock_put):
        create_request_mock(mock_put, FakeResponse(403))
        self.temp.update_client(1, {'name': 'Olek', 'surname':
            'Wardyn', 'email': 'olekwardyn@gmail.com'})
        mock_put.assert_called_once()

    def test_update_client_connection_error(self):
        self.temp.update_client = Mock(side_effect=ConnectionError('Error'))
        assert_that(self.temp.update_client).raises(
            ConnectionError).when_called_with(
            2,
            {
                'name': 'Olek',
                'surname':
                    'Wardyn',
                'email': 'olekwardyn@gmail.com'})

    @patch('src.client.client.requests.delete')
    def test_delete_client_existing(self, mock_delete):
        client_id = 1
        create_request_mock(mock_delete, FakeResponse(200, {'deleted_id':
                                                                client_id}))
        response = self.temp.delete_client(client_id)
        assert_that(response.json['deleted_id']).is_close_to(client_id, 0)

    @patch('src.client.client.requests.delete')
    def test_delete_client_existing_mock_called(self, mock_delete):
        create_request_mock(mock_delete, FakeResponse(200, {'deleted_id': 1}))
        self.temp.delete_client(1)
        mock_delete.assert_called_once()

    def test_delete_client_type_error(self):
        assert_that(self.temp.delete_client).raises(
            TypeError).when_called_with('string')

    def test_delete_client_not_existing(self):
        self.temp.delete_client = MagicMock(
            return_value=FakeResponse(404, error_message="User "
                                                         "does not exists"))
        response = self.temp.delete_client(3)
        assert_that(response.error_message).contains('User', 'not')

    def test_delete_client_not_existing_mock_called(self):
        self.temp.delete_client = MagicMock(
            return_value=FakeResponse(404, error_message="User "
                                                         "does not exists"))
        self.temp.delete_client(3)
        self.temp.delete_client.assert_called_with(3)

    def test_delete_client_connection_error(self):
        self.temp.delete_client = MagicMock(side_effect=ConnectionError(
            'Error'))
        assert_that(self.temp.delete_client).raises(
            ConnectionError).when_called_with(3)

    def test_get_client_order_ok(self):
        client_id = 1
        order_id = 1
        self.temp.get_client_order = Mock()
        self.temp.get_client_order.return_value = FakeResponse(200,
                                                               {'order': [{'name': 'name1', 'value': 10}, {'name': 'name2', 'value': 20}]})  # add
        response = self.temp.get_client_order(client_id, order_id)
        self.assertEqual(response.status_code, 200)

    def test_get_client_order_ok_mock_called(self):
        self.temp.get_client_order = Mock()
        self.temp.get_client_order.return_value = FakeResponse(200,
                                                               {'order': [{'name': 'name1', 'value': 10}, {'name': 'name2', 'value': 20}]})  # add
        self.temp.get_client_order(1, 1)
        self.temp.get_client_order.assert_called_with(1, 1)

    @patch('src.client.client.requests.get')
    def test_get_client_order_not_existing_client(self, mock_get):
        create_request_mock(mock_get, FakeResponse(404,
                                                   error_message='User does not exist'))
        response = self.temp.get_client_order(3, 4)
        self.assertEqual(response.error_message, 'User does not exist')

    @patch('src.client.client.requests.get')
    def test_get_client_order_not_existing_client_mock_called(self, mock_get):
        create_request_mock(mock_get, FakeResponse(404,
                                                   error_message='User does not exist'))
        self.temp.get_client_order(3, 4)
        mock_get.assert_called_once()

    def test_get_client_order_not_existing_order(self):
        self.temp.get_client_order = MagicMock(return_value=FakeResponse(404,
                                                                         error_message="Order does not exists"))
        response = self.temp.get_client_order(1, 10)
        self.assertEqual(response.error_message, 'Order does not exists')

    def test_get_client_order_not_existing_order_mock_called(self):
        self.temp.get_client_order = MagicMock(return_value=FakeResponse(404,
                                                                         error_message="Order does not exists"))
        self.temp.get_client_order(1, 10)
        self.temp.get_client_order.assert_called_once_with(1, 10)

    def test_get_client_order_type_error(self):
        assert_that(self.temp.get_client_order).raises(
            TypeError).when_called_with("id", 3)

    def test_get_client_orders_ok(self):
        client_id = 1
        self.temp.get_client_orders = Mock()
        self.temp.get_client_orders.return_value = FakeResponse(200,
                                                                {'orders': [{'order': [{'name': 'name1', 'value': 10}, {'name': 'name2', 'value': 20}]}, {'order': [{'name': 'name3', 'value': 22}, {'name': 'name2', 'value': 33}]}]})  # add
        # response (dont know what it is right now, stepik went down)
        response = self.temp.get_client_orders(client_id)
        self.assertEqual(response.status_code, 200)

    def test_get_client_orders_ok_mock_called(self):
        self.temp.get_client_orders = Mock()
        self.temp.get_client_orders.return_value = FakeResponse(200,
                                                                {})  # add
        # response (dont know what it is right now, stepik went down)
        self.temp.get_client_orders(1)
        self.temp.get_client_orders.assert_called_with(1)

    @patch('src.client.client.requests.get')
    def test_get_client_orders_not_existing_client(self, mock_get):
        create_request_mock(mock_get, FakeResponse(404, error_message='User '
                                                                      'does not exist'))
        response = self.temp.get_client_orders(3)
        self.assertEqual(response.error_message, 'User does not exist')

    @patch('src.client.client.requests.get')
    def test_get_client_orders_not_existing_client_mock_called(self, mock_get):
        create_request_mock(mock_get, FakeResponse(404, error_message='User '
                                                                      'does not exist'))
        self.temp.get_client_orders(3)
        mock_get.assert_called_once()

    def test_get_client_orders_type_error(self):
        assert_that(self.temp.get_client_orders).raises(
            TypeError).when_called_with("id")

    def tearDown(self) -> None:
        self.temp = None


class FakeResponse(object):
    def __init__(self, status_code, json=None, error_message=None):
        self.status_code = status_code
        self.json = json
        self.error_message = error_message
