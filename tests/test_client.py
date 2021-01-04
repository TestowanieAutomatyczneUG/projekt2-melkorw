import unittest
from unittest import mock
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

    @patch('src.client.client.requests.get')
    def test_get_client_with_id(self, mock_get):
        client_id = 1
        self.temp.get_client = Mock()
        self.temp.get_client.return_value = FakeResponse(200, {'name':
                                                                   'Olek',
                                                               'surname':
                                                                   'Wardyn',
                                                               'email':
                                                                   'olekwardyn@gmail.com', 'id': client_id})
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


class FakeResponse(object):
    def __init__(self, status_code, json=None, error_message=None):
        self.status_code = status_code
        self.json = json
        self.error_message = error_message
