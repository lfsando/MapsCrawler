import csv
import json
import sys

with open(f'{sys.argv[1]}.json', 'r', encoding='utf-8') as f:
    data = json.loads(f.read())

telephones = []
result = []
for p in data:

    tel = p['phone_number']
    if tel in telephones:
        continue
    else:
        result.append(p)

with open(f'{sys.argv[1]}.csv', 'w', encoding='utf-8', newline='') as f:
    dict_writer = csv.DictWriter(f, fieldnames=result[0].keys(), dialect="excel", )
    dict_writer.writeheader()
    dict_writer.writerows(data)
