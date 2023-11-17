from bs4 import BeautifulSoup
import csv, requests, urllib.request, json, progress, re
from progress.bar import *
from fnmatch import fnmatch
from clear import *

#принимает номер CVE yyyy-nnnn[n] (год - 4 знака, номер - 4-5 знаков)
#возвращает таблицу в формате json

def get_table(CVE):
    _url = f'https://api.msrc.microsoft.com/sug/v2.0/en-US/affectedProduct?$orderBy=releaseDate%20desc&$filter=cveNumber%20eq%20%27{CVE}%27'
    with urllib.request.urlopen(_url) as url:
        data = json.load(url)
        return data


def link_getter(chunk, index):
    try:
        return chunk['kbArticles'][ind]['downloadUrl']

    except KeyError:
        return None


def get_link(CVE, platform, product):
    data = get_table(CVE)

    for chunk in data['value']:
        if chunk['product'] == product and chunk['platform'] == platform:
            if chunk['kbArticles'][0]['downloadName'] == "Monthly Rollup":
                return link_getter(chunk, 0)
           
            else:
                return link_getter(chunk, 1)


# foramt : nnnnnnn [7]
def get_kb(KB):
    _url = f'https://catalog.update.microsoft.com/Search.aspx?q=KB{KB}'
    response = requests.get(_url)
    return response.text



def main():
    with open('obraz.csv', 'r', encoding='utf-8', newline='') as file:
        bar = ChargingBar("Просчитано: ", max=1142)
        reader = csv.DictReader(file)
        counter = 0

        for row in reader:
            for cve in row['CVE'].split(','):            
                cve = cve.lstrip().rstrip()
           
                try:
                    link = get_link(cve, row['OS'], row['PO'])
                    if link != None:
                        counter += 1

                except:
                    print('Err')

            bar.next()

        print(counter, f'{(counter/1142 * 100)} %')

            

if __name__ == '__main__':
    main()
