import requests
from lib.assertions import Assertions
from lib.base_case import BaseCase


class TestUserGet(BaseCase):
    expected_fields = ["lastName", "firstName", "email"]

    def test_get_user_details_not_auth(self):
        response = requests.get("https://playground.learnqa.ru/api/user/2")
        print(response.content)
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_keys(response, self.expected_fields)

    def test_get_user_auth(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.x_csrf_token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": self.x_csrf_token},
            cookies={"auth_sid": self.auth_sid}
        )
        expected_fields = ["username", "lastName", "firstName", "email"]

        Assertions.assert_json_has_keys(response2, expected_fields)

    def test_get_data_some_user(self):
        register_data = self.prepare_registration_data()
        response_1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_status_code(response_1, 200)
        Assertions.assert_json_has_key(response_1, "id")
        user_id_1 = self.get_json_value(response_1, "id")
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response_2 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        self.auth_sid = self.get_cookie(response_2, "auth_sid")
        self.x_csrf_token = self.get_header(response_2, "x-csrf-token")

        response_3 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id_1}",
            headers={"x-csrf-token": self.x_csrf_token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_json_has_key(response_3, "username")
        Assertions.assert_json_has_not_keys(response_3, self.expected_fields)
