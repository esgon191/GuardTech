import requests
from bs4 import BeautifulSoup
from exceptions import * 
from functools import lru_cache
# ссылка, которую я получаю из прошлой функции
@lru_cache(maxsize=None)
def get_stage2_link(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.837 YaBrowser/23.9.4.837 Yowser/2.5 Safari/537.36"
    }

    textcode = requests.get(url, headers = head).text
    soup = BeautifulSoup(textcode, 'lxml')

    count = 0
    all_links = []

    # строки таблицы, содержащие нужную нам информацию: id для получения ссылки и количество продуктов(нужен больший)
    try:
        all_import_lines = soup.find(class_ = 'resultsBackGround').find('table').find_all('tr')

    except AttributeError:
        raise NoStage2DataError()

    for item in all_import_lines:
        row = []
        if count != 0:
            item_id = item.get('id')
            item_id = item_id[:-3]
            # создаем ссылку
            row.append('https://www.catalog.update.microsoft.com/ScopedViewInline.aspx?updateid=' + str(item_id))
            words = item.find_all('td')
            # получаем названия каждой ячейки с каждой линии
            for word in words:
                row.append(word.text)
            all_links.append(row)
        count += 1
    final_links = []

    # добавляем в final_links толлько интересующие нас данные [link, number of versions]
    for li in all_links:
        final_links.append([li[0], len(li[3].split(','))])
    max_link = '' # то, что нас интересует в данной функции. Самое главное
    max_count = 0

    # зная количество версий, находим нужную нам ссылку
    for line in final_links:
        if line[1] > max_count:
            max_count = line[1]
            max_link = line[0]

    #возвращает updateid
    return max_link.split('updateid=')[-1]

