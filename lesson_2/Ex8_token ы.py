import requests
import time

create_task = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")

wait = create_task.json()["seconds"] + 1
params = {
    "token": create_task.json()["token"]
}

response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=params)
status_before = response.json()["status"]

if status_before == "Job is NOT ready":
    time.sleep(wait)
    response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=params)
    result_json = response.json()
    if result_json["status"] == "Job is ready":
        print("Поле status заполнено корректно.")
    else:
        print("Поле status не соответвует ОР: 'Job is ready'")
    if result_json["result"] is not None:
        print(f'Поле result не пустое: {result_json["result"]}')
    else:
        print("Поле result пустое")
else:
    print("Значение поля 'status' до готовности задачи не соответсвует тексу: 'Job is NOT ready'")
