from progress.bar import *
import csv
counter = 0

#Анализ исходных файлов
#

with open('svod.csv', 'r', encoding='utf-8', newline='') as file:
    bar = ChargingBar("Просчитано: ", max=1142)
    reader = csv.DictReader(file)
    for row in reader:
        string = row['OS'] + row['PO']
        for word in string.split(' '):
            counter += 1
data = []
with open('svod.csv', 'r', encoding='utf-8', newline='') as file:
    bar = ChargingBar("Просчитано: ", max=counter)
    reader = csv.DictReader(file)
    for row in reader:
        string = row['OS'] + row['PO']
        if 'Microsoft' in row['PO']:
            for word in string.split(' '):
                data.append(word)
            

data = set(data)
print(counter, len(list(data)), f'{len(list(data))/counter * 100}%')
for i in data:
    print(i)
