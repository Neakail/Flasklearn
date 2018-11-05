import requests
import json

def readfile(filename):
    with open(filename, 'r') as fp:
        data = json.load(fp, encoding='utf-8')
    return data

news_set = readfile('woshigeshou.json')

a = requests.post(url='http://127.0.0.1:5000/process',data=json.dumps(news_set))
print a.text

