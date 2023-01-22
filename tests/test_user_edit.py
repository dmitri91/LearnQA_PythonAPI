import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
from random import choice
from string import ascii_lowercase


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # register
        register_data = self.prepare_registration_data()
        response_1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_status_code(response_1, 200)
        Assertions.assert_json_has_key(response_1, "id")

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

        # edit
        new_name = "ivan"
        response_3 = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": self.x_csrf_token},
            cookies={"auth_sid": self.auth_sid},
            data={'firstName': new_name}
        )

        Assertions.assert_status_code(response_3, 200)
        # get
        response_4 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": self.x_csrf_token},
            cookies={"auth_sid": self.auth_sid},
        )

        Assertions.assert_json_value_by_name(
            response_4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    def test_edit_not_auth_user(self):
        # register
        register_data = self.prepare_registration_data()
        response_1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_status_code(response_1, 200)
        Assertions.assert_json_has_key(response_1, "id")
        user_id = self.get_json_value(response_1, "id")

        # edit
        new_name = "ivan"
        response_2 = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            data={'firstName': new_name}
        )
        Assertions.assert_status_code(response_2, 400)
        assert response_2.content.decode("utf-8") == "Auth token not supplied", \
            f"Unexpected response content:{response_2.content}"

    def test_edit_other_user(self):
        # register first user
        register_data_1 = self.prepare_registration_data()
        response_1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data_1)

        Assertions.assert_status_code(response_1, 200)
        user_id_1 = self.get_json_value(response_1, "id")
        email_1 = register_data_1['email']
        firs_name_1 = register_data_1['firstName']
        last_name_1 = register_data_1['lastName']
        password_1 = register_data_1['password']
        user_name_1 = register_data_1['username']

        # register second user
        register_data_2 = self.prepare_registration_data()
        response_2 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data_2)

        Assertions.assert_status_code(response_2, 200)

        email_2 = register_data_2['email']
        password_2 = register_data_2['password']

        # login second user
        data = {
            'email': email_2,
            'password': password_2
        }
        response_3 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        self.auth_sid_2 = self.get_cookie(response_3, "auth_sid")
        self.x_csrf_token_2 = self.get_header(response_3, "x-csrf-token")

        # edit
        new_firs_name = "ivanko"
        new_last_name = "smirnov"
        new_user_name = "i.smirnov"
        response_4 = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id_1}",
            headers={"x-csrf-token": self.x_csrf_token_2},
            cookies={"auth_sid": self.auth_sid_2},
            data={
                'username': new_user_name,
                'firstName': new_firs_name,
                'lastName': new_last_name,
            })
        Assertions.assert_status_code(response_4, 200)

        # login first user
        data = {
            'email': email_1,
            'password': password_1
        }
        response_5 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        self.auth_sid_1 = self.get_cookie(response_5, "auth_sid")
        self.x_csrf_token_1 = self.get_header(response_5, "x-csrf-token")

        # get first user
        response_6 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id_1}",
            headers={"x-csrf-token": self.x_csrf_token_1},
            cookies={"auth_sid": self.auth_sid_1},
        )
        expected_fields = [firs_name_1, last_name_1, user_name_1]
        parameter = ['firstName', 'lastName', 'username']
        for value, par in zip(expected_fields, parameter):
            Assertions.assert_json_value_by_name(
                response_6,
                par,
                value,
                "Wrong name of the user after edit"
            )

    def test_edit_email(self):
        # register
        register_data = self.prepare_registration_data()
        response_1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_status_code(response_1, 200)
        Assertions.assert_json_has_key(response_1, "id")

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

        # edit
        email = email.replace('@', '')
        random_part = datetime.now().strftime("%M%S")
        new_email = f"{random_part}{email}"

        response_3 = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": self.x_csrf_token},
            cookies={"auth_sid": self.auth_sid},
            data={'email': new_email}
        )

        Assertions.assert_status_code(response_3, 400)
        assert response_3.content.decode("utf-8") == "Invalid email format", \
            f"Unexpected response content:{response_3.content}"

    def test_edit_shot_firstname(self):
        # register
        register_data = self.prepare_registration_data()
        response_1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_status_code(response_1, 200)
        Assertions.assert_json_has_key(response_1, "id")

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

        # edit
        new_name = "".join(choice(ascii_lowercase) for i in range(1))
        response_3 = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": self.x_csrf_token},
            cookies={"auth_sid": self.auth_sid},
            data={'firstName': new_name}
        )
        Assertions.assert_status_code(response_3, 400)
        assert response_3.content.decode("utf-8") == '{"error":"Too short value for field firstName"}', \
            f"Unexpected response content:{response_3.content}"
