import requests
from lib.assertions import Assertions
from lib.base_case import BaseCase


class TestUserDelete(BaseCase):

    def test_delete_user_id_2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response_1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        auth_sid = self.get_cookie(response_1, "auth_sid")
        x_csrf_token = self.get_header(response_1, "x-csrf-token")
        user_id = self.get_json_value(response_1, "user_id")

        response_2 = requests.delete(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": x_csrf_token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_status_code(response_2, 400)
        assert response_2.content.decode("utf-8") == 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.', \
            f"Unexpected response content:{response_2.content}"

    def test_delete_user(self):
        # register
        register_data = self.prepare_registration_data()
        response_1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_status_code(response_1, 200)

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response_1, "id")

        # login
        data = {
            'email': email,
            'password': password
        }
        response_2 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        self.auth_sid = self.get_cookie(response_2, "auth_sid")
        self.x_csrf_token = self.get_header(response_2, "x-csrf-token")

        # delete
        response_3 = requests.delete(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": self.x_csrf_token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_status_code(response_3, 200)

        # get
        response_4 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": self.x_csrf_token},
            cookies={"auth_sid": self.auth_sid}
        )
        Assertions.assert_status_code(response_2, 200)
        assert response_4.content.decode("utf-8") == 'User not found', \
            f"Unexpected response content:{response_4.content}"

    def test_delete_other_user(self):
        # register first user
        register_data_1 = self.prepare_registration_data()
        response_1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data_1)

        username_1 = register_data_1['username']
        Assertions.assert_status_code(response_1, 200)
        user_id_1 = self.get_json_value(response_1, "id")

        # register second user
        register_data_2 = self.prepare_registration_data()
        response_2 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data_2)

        Assertions.assert_status_code(response_2, 200)

        email_2 = register_data_2['email']
        password_2 = register_data_2['password']
        #user_id = self.get_json_value(response_2, "id")

        # login second user
        data = {
            'email': email_2,
            'password': password_2
        }
        response_3 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        self.auth_sid = self.get_cookie(response_3, "auth_sid")
        self.x_csrf_token = self.get_header(response_3, "x-csrf-token")

        # delete first user
        response_4 = requests.delete(
            f"https://playground.learnqa.ru/api/user/{user_id_1}",
            headers={"x-csrf-token": self.x_csrf_token},
            cookies={"auth_sid": self.auth_sid}
        )
        # get first user
        response_5 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id_1}")

        Assertions.assert_status_code(response_5, 200)
        Assertions.assert_json_value_by_name(
            response_5,
            "username",
            username_1,
            f"User with 'username':{user_id_1} not found"
        )
