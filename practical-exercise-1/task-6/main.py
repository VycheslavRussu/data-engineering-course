import requests
import json

url = 'http://apilayer.net/api/live'
accessKey = 'b6753cb92ea2bd37426cb63a181d4034'
params = {'access_key': accessKey, 'currencies': 'RUB', 'source': 'USD', 'format': '1'}
responseJson = requests.get(url, params=params).json()

USDRUB = responseJson['quotes']['USDRUB']

html = f"<h1>Стоимость 1 доллара {USDRUB} </h1>"
with open("answer_6_var_65.html", "w", encoding="utf-8") as output:
    output.write(html)