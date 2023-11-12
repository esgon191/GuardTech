from progress.bar import *
import csv
counter = 0

#Анализ исходных файлов
counters = {
    'PO' : 0,
    'OS' : 0
}

with open('svod.csv', 'r', encoding='utf-8', newline='') as file:
    bar = ChargingBar("Просчитано: ", max=1142)
    reader = csv.DictReader(file)
    for row in reader:
        counter += len(row['PO'].split(' - '))
        counter += len(row['OS'].split(' - '))


data = {key : [] for key in counters.keys()}

with open('svod.csv', 'r', encoding='utf-8', newline='') as file:
    bar = ChargingBar("Просчитано: ", max=counter)
    reader = csv.DictReader(file)
    for row in reader:
        for key in data.keys():
            elem = list(row[key].split(' - '))
            for i in range(len(elem)):
                data[key].append(elem[i])

for key in data.keys():
    data[key] = set(data[key])
    for elem in data[key]:
        print(*elem.split(' '))
    print('\n')
