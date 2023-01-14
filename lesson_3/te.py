import requests

data = {'email' : 'vinkotov@example.com', 'password' : '1234'}
respon = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

print(respon.json())