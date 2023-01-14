import requests


def test_check_cookie():
    response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
    print(dict(response.cookies))
    assert 'HomeWork' in response.cookies, "There is not cookie in the response"
    assert 'hw_value' in dict(response.cookies)['HomeWork'], 'There is incorrect value cookie in the response'
