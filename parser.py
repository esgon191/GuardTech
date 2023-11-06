import requests
from bs4 import BeautifulSoup
import urllib.request, json

#принимает номер CVE yyyy-nnnn[n] (год - 4 знака, номер - 4-5 знаков)
#возвращает таблицу в формате json

def get_table(CVE):
    _url = f'https://api.msrc.microsoft.com/sug/v2.0/en-US/affectedProduct?$orderBy=releaseDate%20desc&$filter=cveNumber%20eq%20%27CVE-{CVE}%27'
    with urllib.request.urlopen(_url) as url:
        data = json.load(url)
        return data
