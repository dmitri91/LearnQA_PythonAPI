import requests


def test_check_header():
    response = requests.get("https://playground.learnqa.ru/api/homework_header")
    print(response.headers)
    assert 'x-secret-homework-header' in response.headers, "There is not header in the response"
    assert 'Some secret value' == response.headers['x-secret-homework-header'], 'There is incorrect value headers in the response'
