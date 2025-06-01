import datetime
import hashlib
import unittest

from types import SimpleNamespace

import pytest
from src import api
from src.utils import retry_decorator

ADMIN_SALT = "42"
SALT = "Otus"


def make_valid_admin_token():
    return hashlib.sha512(
        (datetime.datetime.now().strftime("%Y%m%d%H") + ADMIN_SALT).encode('utf-8')
    ).hexdigest()

def make_valid_user_token(request):
    return hashlib.sha512(
            (request.account + request.login + SALT).encode('utf-8')
        ).hexdigest()


class TestSuite(object):
    context = {}
    headers = {}
    store = None
    repository = None

    def get_response(self, request):
        return api.method_handler({"body": request, "headers": self.headers}, self.context, self.store)

    def test_empty_request(self):
        response, code = self.get_response({})
        assert code == api.INVALID_REQUEST

    @pytest.mark.parametrize("request_data, expected_code", [
        pytest.param({"account": "horn&hoofs", "login": "h&f", "method": "online_score", "token": "", "arguments": {}},
                     403, id='Authorization without token'),
        pytest.param(
            {"account": "horn&hoofs", "login": "h&f", "method": "online_score", "token": "wrongtoken", "arguments": {}},
            403, id='Authorization with a wrong token'),
        pytest.param(
            {"account": "horn&hoofs", "login": "admin", "method": "online_score", "token": make_valid_admin_token(),
             "arguments": {}}, 200, id='Authorization under admin'),
    ])
    def test_bad_auth(self, request_data, expected_code):
        response, code = self.get_response(request_data)
        assert code == expected_code

    def test_get_score_ignores_store_errors(self, mocker):
        mock_store = mocker.Mock()
        mock_store.get.side_effect = Exception('Store is not available')


        request = {
            "account": "horn&hoofs",
            "login": "admin",
            "method": "online_score",
            "token": make_valid_admin_token(),
            "arguments": {
                "phone": "71234567890",
                "email": "email@example.com",
            }
        }

        self.store = mock_store
        response, code = self.get_response(request)

        assert code == 200
        assert "score" in response


    def test_get_interests_fails_on_store_error(self, mocker):
        mock_store = mocker.Mock()

        mock_store.get.side_effect = Exception('Store is unavailable')


        request_data = {
            "account": "horn&hoofs",
            "login": "some_user",
            "method": "clients_interests",
            "token": "",
            "arguments": {
                "client_ids": [1, 2, 3],
                "date": "20.05.2004",
            }
        }

        request_object = SimpleNamespace(**request_data)
        request_object.token = make_valid_user_token(request_object)
        request_data['token'] = request_object.token


        self.store = mock_store

        response, code = self.get_response(request_data)

        assert code == 500


    def test_retry_decorator(self, mocker):
        mock_fn = mocker.Mock()
        mock_fn.side_effect = [
            Exception('Retry #1'),
            Exception('Retry #2'),
            'success'
        ]

        @retry_decorator(timeout=0, retry_times=3)
        def flaky_function():
            return mock_fn()

        result = flaky_function()
        assert result == "success"
        assert mock_fn.call_count == 3



if __name__ == "__main__":
    unittest.main()
