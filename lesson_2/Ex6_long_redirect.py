import requests

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh)'
}

response = requests.get("https://playground.learnqa.ru/api/long_redirect", headers=header)

number_redirects = len(response.history)
print("Kоличество редиректов:", number_redirects)
url_end = response.url
print("Конечный URL:", url_end)
