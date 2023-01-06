import requests

#1.http-запрос любого типа без параметра method
params_1 = {}
response_1 = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=params_1)
print("Ответ без параметра method:", response_1.text)

#2.http-запрос не из списка. Например, HEAD.
params_2 = {
    "method": "HEAD"
}
response_2 = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=params_2)
print("Ответ с параметром не из списка:", response_2.text)

#3.Запрос с правильным значением method
params_3 = {
    "method": "GET"
}
response_3 = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=params_3)
print("Ответ с правильным значением method:", response_3.text)

#4.Проверка сочетания реальных типов запроса и значений параметра method
value_methods = ["GET", "POST", "PUT", "DELETE"]

for i in value_methods:
    type_method = {
        "method": f"{i}"
    }

    response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=type_method)
    if i == "GET" and response.text != '{"success":"!"}':
        print(f"GET request and method=GET -> {response.text}")
    elif i != "GET" and response.text == '{"success":"!"}':
        print(f"GET request and method={i} -> {response.text}")

    response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data=type_method)
    if i == "POST" and response.text != '{"success":"!"}':
        print(f"POST request and method=POST -> {response.text}")
    elif i != "POST" and response.text == '{"success":"!"}':
        print(f"POST request and method={i} -> {response.text}")

    response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data=type_method)
    if i == "PUT" and response.text != '{"success":"!"}':
        print(f"PUT request and method=PUT -> {response.text}")
    elif i != "PUT" and response.text == '{"success":"!"}':
        print(f"PUT request and method={i} -> {response.text}")

    response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data=type_method)
    if i == "DELETE" and response.text != '{"success":"!"}':
        print(f"DELETE request and method=DELETE-> {response.text}")
    elif i != "DELETE" and response.text == '{"success":"!"}':
        print(f"DELETE request and method={i} -> {response.text}")