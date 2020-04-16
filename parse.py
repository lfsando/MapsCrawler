import csv
import json

with open('data1.json', 'r', encoding='utf-8') as f:
    data = json.loads(f.read())

with open('lista-de-empresas2.csv', 'w', encoding='utf-8', newline='') as f:
    dict_writer = csv.DictWriter(f, fieldnames=data[0].keys(), dialect="excel", )
    dict_writer.writeheader()
    dict_writer.writerows(data)
