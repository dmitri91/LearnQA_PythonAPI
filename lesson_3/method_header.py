import requests


def test_check_header():
    response = requests.get("https://playground.learnqa.ru/api/homework_header")
    print(response.text)
    assert 'success' in response.text, "There is not header in the response"
    assert '!' == (response.json())['success'], 'There is incorrect value headers in the response'
