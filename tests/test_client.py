import unittest
from assertpy import *
from unittest.mock import *
from client.client import Client


class ClientTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = Client()

    @patch('src.client.client.requests.post')
    def test_add_client(self, mock_post):
        mock_post.return_value = Mock(ok=True)
        mock_post.return_value.status_code = 201
        mock_post.return_value.json = {'id': 1}
        response = self.temp.add_client({'name': 'Olek', 'surname':
            'Wardyn', 'email': 'olekwardyn@gmail.com'})
        assert_that(response.status_code).is_between(200, 299)
        assert_that(response.json).is_not_none()
        self.assertTrue(mock_post.called)
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
        mock_post.return_value = Mock(ok=True)
        mock_post.return_value.status_code = 409
        response = self.temp.add_client({'name': 'Olek', 'surname':
            'Wardyn', 'email': 'olekwardyn@gmail.com'})
        assert_that(response).is_equal_to('User of given email exists')
        mock_post.assert_called_once()

    @patch('src.client.client.requests.post')
    def test_add_client_other_errors(self, mock_post):
        mock_post.return_value = Mock(ok=True)
        mock_post.return_value.status_code = 404
        response = self.temp.add_client({'name': 'Olek', 'surname':
            'Wardyn', 'email': 'olekwardyn@gmail.com'})
        assert_that(response).contains('error')
        mock_post.assert_called_once()

    def test_get_client_with_id(self):
        client_id = 1
        self.temp.get_client = Mock()
        self.temp.get_client.return_value = FakeResponse(200, {'name':
                                                                   'Olek',
                                                               'surname':
                                                                   'Wardyn',
                                                               'email':
                                                                   'olekwardyn@gmail.com',
                                                               'id': client_id})
        response = self.temp.get_client(client_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], 'olekwardyn@gmail.com')
        self.assertEqual(response.json['id'], client_id)
        self.temp.get_client.assert_called_with(client_id)

    @patch('src.client.client.requests.get')
    def test_get_client_not_existing_client(self, mock_get):
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.status_code = 404
        response = self.temp.get_client(2)
        self.assertEqual(response, 'User does not exist')

    def test_get_client_id_type_error(self):
        assert_that(self.temp.get_client).raises(
            TypeError).when_called_with('id')

    def test_get_client_internet_error(self):
        self.temp.get_client = Mock(side_effect=Exception('Exception'))
        assert_that(self.temp.get_client).raises(Exception).when_called_with(1)

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
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['results']), 2)
        self.temp.get_clients.assert_called_once()

    def test_get_clients_connection_error(self):
        self.temp.get_clients = Mock(side_effect=Exception('Exception'))
        assert_that(self.temp.get_clients).raises(Exception)

    @patch('src.client.client.requests.put')
    def test_update_client(self, mock_put):
        client_id = 1
        mock_put.return_value = Mock(ok=True)
        mock_put.return_value.status_code = 200
        mock_put.return_value.json = {'id': client_id}
        response = self.temp.update_client(client_id, {'name': 'Olek',
                                                       'surname':
                                                           'Wardyn2',
                                                       'email': 'olekwardyn@gmail.com'})
        assert_that(response.status_code).is_between(200, 299)
        assert_that(response.json['id']).is_equal_to(client_id)
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
            ValueError).when_called_with(2, {'name': 'Olek', 'surname':
            'Wardyn'})

    def test_update_client_existing_email(self):
        self.temp.update_client = Mock()
        self.temp.update_client.return_value = FakeResponse(409,
                                                            error_message='Email already exists')
        response = self.temp.update_client(1, {'name': 'Olek', 'surname':
            'Wardyn', 'email': 'olekwardyn@gmail.com'})
        assert_that(response.error_message).is_equal_to('Email already exists')
        self.temp.update_client.assert_called_once()

    @patch('src.client.client.requests.put')
    def test_update_client_user_does_not_exist(self, mock_put):
        mock_put.return_value = Mock(ok=True)
        mock_put.return_value.status_code = 404
        mock_put.return_value.error_message = 'User does not exist'
        response = self.temp.update_client(3, {'name': 'Olek', 'surname':
            'Wardyn', 'email': 'olekwardyn@gmail.com'})
        assert_that(response.error_message).contains('does', 'not')
        mock_put.assert_called_once()

    @patch('src.client.client.requests.put')
    def test_update_client_other_errors(self, mock_put):
        mock_put.return_value = Mock(ok=True)
        mock_put.return_value.status_code = 403
        response = self.temp.update_client(1, {'name': 'Olek', 'surname':
            'Wardyn', 'email': 'olekwardyn@gmail.com'})
        assert_that(response).is_equal_to_ignoring_case('SOMETHING WENT '
                                                        'HORRIBLY WRONG')
        mock_put.assert_called_once()

    def test_update_client_connection_error(self):
        self.temp.update_client = Mock(side_effect=Exception('Exception'))
        assert_that(self.temp.get_clients).raises(Exception).when_called_with(2,
                                                                         {
                                                                             'name': 'Olek',
                                                                             'surname':
                                                                                 'Wardyn',
                                                                             'email': 'olekwardyn@gmail.com'})

    @patch('src.client.client.requests.delete')
    def test_delete_client_existing(self, mock_delete):
        client_id = 1
        mock_delete.return_value = Mock(ok=True)
        mock_delete.return_value.status_code = 200
        mock_delete.return_value.json = {'deleted_id': client_id}
        response = self.temp.delete_client(client_id)
        assert_that(response.status_code).is_between(200, 299)
        assert_that(response.json['deleted_id']).is_close_to(client_id, 0)
        mock_delete.assert_called_once()

    def test_delete_client_type_error(self):
        assert_that(self.temp.delete_client).raises(
            TypeError).when_called_with('string')

    def test_delete_client_not_existing(self):
        self.temp.delete_client = MagicMock(return_value=FakeResponse(404, error_message="User "
                                                                      "does not exists"))
        response = self.temp.delete_client(3)
        assert_that(response.status_code).is_greater_than(399)
        assert_that(response.json).is_none()
        assert_that(response.error_message).contains('User', 'not')
        self.temp.delete_client.assert_called_with(3)


class FakeResponse(object):
    def __init__(self, status_code, json=None, error_message=None):
        self.status_code = status_code
        self.json = json
        self.error_message = error_message
