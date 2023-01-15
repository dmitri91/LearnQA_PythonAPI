import requests
import pytest

user_agent_1 = "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"
expected_values_1 = {'platform': 'Mobile', 'browser': 'No', 'device': 'Android'}

user_agent_2 = 'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1'
expected_values_2 = {'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'}

user_agent_3 = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
expected_values_3 = {'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'}

user_agent_4 = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0'
expected_values_4 = {'platform': 'Web', 'browser': 'Chrome', 'device': 'No'}

user_agent_5 = 'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
expected_values_5 = {'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'}

data_test = [
    (user_agent_1, expected_values_1),
    (user_agent_2, expected_values_2),
    (user_agent_3, expected_values_3),
    (user_agent_4, expected_values_4),
    (user_agent_5, expected_values_5)
]


@pytest.mark.parametrize("user_agent, expected_values", data_test)
def test_check_user_agent(user_agent, expected_values):
    response = requests.get(" https://playground.learnqa.ru/ajax/api/user_agent_check", headers={"User-Agent": f"{user_agent}"})
    assert "platform" in response.json(), f"There is not field 'platform' in the response for user_agent: {user_agent}"
    assert "browser" in response.json(), f"There is not field 'browser' in the response for user_agent: {user_agent}"
    assert "device" in response.json(), f"There is not field 'device' in the response for user_agent: {user_agent}"

    fields = ["platform", "browser", "device"]
    for i in fields:
        if response.json()[i] == "Unknown":
            print(f"В user_agent: {user_agent} вренулся неправильный параметр:{i}")
