import csv

def read_file(nazv: str) -> list:
    '''
    Считывает файл и возвращает массив словарей
    '''
    res = []
    with open(nazv, 'r', encoding='utf-8', newline='') as input_file:
        reader = csv.DictReader(input_file)        
        for row in reader:
            res.append(row)

    return res

with open('svod.csv', 'w', encoding='utf-8', newline='') as output_file:
    '''
    Свод трех исходных файлов в один.
    Нужно лишь для теста.
    '''
    files_to_svod = ['obraz1.csv',
                     'obraz2.csv',
                     'obraz3.csv']
    
    fieldnames = ['OS', 
                  'CVE',
                  'PO']

    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()

    for file in files_to_svod:
        for row in read_file(file):
            writer.writerow({
                'OS' : row['Операционная система'],
                'CVE' : row['CVE'],
                'PO' : row['Сервис/ПО'],
                })
