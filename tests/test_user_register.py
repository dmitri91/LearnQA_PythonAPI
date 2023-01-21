import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
import pytest
from random import choice
from string import ascii_lowercase

TEST_URL = "https://playground.learnqa.ru/api/user/"
class TestUserRegister(BaseCase):
    def setup_method(self):
        base_part = "novgorod"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        email = f"{base_part}{random_part}@{domain}"
        self.data = {
            'password': "1234",
            'username': "ld",
            'firstName': "dima",
            'lastName': "dima",
            'email': email
        }

    def test_create_user_successfully(self):
        response = requests.post(TEST_URL, data=self.data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_incorrect_email(self):
        email = self.data['email'].replace('@', '')
        self.data['email'] = email
        response = requests.post(TEST_URL, data=self.data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format",\
            f"Unexpected response content:{response.content}"

    parameter_list = [('password'), ('username'), ('firstName'), ('lastName'), ('email')]

    @pytest.mark.parametrize("parameter", parameter_list)
    def test_create_user_without_parameter(self, parameter):
        del self.data[parameter]
        response = requests.post(TEST_URL, data=self.data)
        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {parameter}", \
            f"Unexpected response content:{response.content}"

    def test_create_user_short_name(self):
        short_val = "".join(choice(ascii_lowercase) for i in range(1))
        self.data['username'] = short_val
        response = requests.post(TEST_URL, data=self.data)
        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too short", \
            f"Unexpected response content:{response.content}"

    def test_create_user_long_name(self):
        long_val = "".join(choice(ascii_lowercase) for i in range(250))
        self.data['username'] = long_val
        response = requests.post(TEST_URL, data=self.data)
        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")
