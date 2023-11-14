from bs4 import BeautifulSoup
import csv, requests, urllib.request, json, progress
from progress.bar import *
from fnmatch import fnmatch
def get_table(CVE):
    _url = f'https://api.msrc.microsoft.com/sug/v2.0/en-US/affectedProduct?$orderBy=releaseDate%20desc&$filter=cveNumber%20eq%20%27{CVE}%27'
    with urllib.request.urlopen(_url) as url:
        data = json.load(url)
        return data


def one():
    counters = {
    'PO' : 0,
    'OS' : 0
    }
    counter_not_found = 0
    with open('svod.csv', 'r', encoding='utf-8', newline='') as file:
        bar = ChargingBar('Done', max=2800)
        reader = csv.DictReader(file)
        for row in reader:
            try:
                data = get_table(row['CVE'])
                for chunk in data['value']:
                    counters['PO'] += 1
                    counters['OS'] += 1
            except:
                counter_not_found += 1

            bar.next()

counters = {'PO': 59665, 'OS': 59665}
data = {key : [] for key in counters.keys()}
runtimes = 0
with open('svod.csv', 'r', encoding='utf-8', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        try:
            for cve in row['CVE'].split(','):
                request = get_table(cve)
                print('requested', cve, end=' ')
                if request['@odata.count'] == 0:
                    raise ValueError

                for chunk in request['value']:
                    data['PO'].append(chunk['product'])
                    try:
                        data['OS'].append(chunk['platform'])
                    except KeyError:
                        data['PO'].append(chunk['product'])


                print('successful')

        except KeyError:
            runtimes += 1
            print('failed:KeyError')

        except ValueError:
            print('failed:EmptyTable')



for key in data.keys():
    data[key] = set(data[key])
    for elem in data[key]:
        print(*elem.split(' '))
    print('\n')
print(runtimes)

for key in counters.keys():
    print(counters[key], len(list(data[key]))/counters[key])