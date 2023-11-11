from progress.bar import *
import csv
counter = 0

with open('obraz.csv', 'r', encoding='utf-8', newline='') as file:
    bar = ChargingBar("Просчитано: ", max=1142)
    reader = csv.DictReader(file)
    for row in reader:
        string = row['OS'] + row['PO']
        for word in string.split(' '):
            counter += 1
data = []
with open('obraz.csv', 'r', encoding='utf-8', newline='') as file:
    bar = ChargingBar("Просчитано: ", max=counter)
    reader = csv.DictReader(file)
    for row in reader:
        string = row['OS'] + row['PO']
        for word in string.split(' '):
            data.append(word)
            

data = set(data)
print(counter, len(list(data))/counter * 100, ' %', data)
