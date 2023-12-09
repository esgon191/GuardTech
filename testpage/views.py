import json
import os
import re
import time
import urllib.request
from functools import lru_cache

import html_to_json as hj
import pandas as pd
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from openpyxl import Workbook

from .clear import format_api, format_local
from .exceptions import *
from .models import Cve

# url = 'https://www.catalog.update.microsoft.com/Search.aspx?q=KB4019114'
main_link = "https://catalog.update.microsoft.com/ScopedView.aspx?updateid="
package_details = "#PackageDetails"
user_file_path = None


def markup(product: str) -> dict:
    '''
    Размечает строку по шаблону для дальнейшего сравнения.
    Позволяет определить, что за продукт перед нами.
    '''

    # дальнейшие функции проверяют принадлежность
    # слова из продукта к какому-то из атрибутов
    def is_razr(atribute: str) -> bool:
        # является ли разрядностью
        reg = r'^(x|arm)*(32|64)(-based|-bit)?$'

        if re.fullmatch(reg, atribute) != None:
            match = re.fullmatch(reg, atribute)[0]
            if 'arm' in match:
                return 'arm' + ''.join([i for i in match if i.isdigit()])

            else:
                return ''.join([i for i in match if i.isdigit()])

    def is_version(atribute: str) -> bool:
        # является ли версией
        reg = r'^([0-9]+\.)[0-9+](.[0-9])*'

        if re.fullmatch(reg, atribute) != None:
            return re.fullmatch(reg, atribute)[0]

    marked_up = {
        'keywords': [],  # ключевые слова
        'versions': [],  # список списков версий, промежутков версий продукта
        'razr': None,  # разрядность
    }

    product = product.split(' ')
    to_skip = 0

    for i in range(len(product)):
        if to_skip > 0:
            to_skip -= 1
            continue

        if product[i] == 'includes':
            marked_up['versions'].append((product[i + 1], product[i + 3]))
            to_skip = 3

        elif is_razr(product[i]) != None:
            marked_up['razr'] = is_razr(product[i])

        elif is_version(product[i]) != None:
            marked_up['versions'].append(is_version((product[i])))

        else:
            marked_up['keywords'].append(product[i])

    marked_up['keywords'].sort()

    if '' in marked_up['keywords']:
        marked_up['keywords'].remove('')

    return marked_up


def rate_match(atr_local: (list | str), atr_api: (list | str), type_of_atr: str) -> int:
    '''
    Оценивает насколько совпадают передаваемые атрибуты
    Возвращает Число от 0 до 2
    '''
    match type_of_atr:
        case 'keywords':
            atr_api = set(atr_api)
            atr_local = set(atr_local)

            if atr_api == atr_local:
                return 2

            elif atr_local <= atr_api or atr_local >= atr_api:
                return 1

            else:
                return 0

        case 'versions':
            if len(atr_api) == 0 and len(atr_local) == 0:
                return 2

            elif len(atr_api) == 0 or len(atr_local) == 0:
                return 1

            for version in atr_api:
                match version:
                    case str():
                        if atr_local[0] == version:
                            return 2

                    case tuple():
                        def format_version(v):
                            # "16.2.8" -> [16, 2, 8]
                            return [int(i) for i in v.split('.')]

                        def format_length(array, length):
                            for i in range(abs(len(array) - length)):
                                array.append(0)

                            return array

                        start = format_version(version[0])
                        end = format_version(version[1])
                        current = format_version(atr_local[0])

                        length = max([len(i) for i in [start, end, current]])

                        start = format_length(start, length)
                        end = format_length(end, length)
                        current = format_length(current, length)

                        flag = True
                        for i in range(len(current)):
                            if current[i] > end[i] or current[i] < start[i]:
                                flag = False

                            elif current[i] < end[i] and current[i] > start[i]:
                                break

                        if flag:
                            return 2

            return 0

        case 'razr':
            if atr_api == None or atr_local == None:
                return 1

            elif atr_api == atr_local:
                return 2

            else:
                return 0


def compare(product_api: str, product_local: str) -> list:
    '''
    Устанавливает, являются ли две строки разными
    названиями одного продукта
    '''

    product_local = format_local(product_local)
    product_api = format_api(product_api)

    product_local = markup(product_local)
    product_api = markup(product_api)

    rating = []
    for key in product_api.keys():
        rating.append(rate_match(product_local[key], product_api[key], key))

    return rating


def get_table(CVE: str) -> dict:
    '''
    Возвращает ссылку по CVE
    Формат: CVE-yyyy-nnnn; Пример: CVE-2017-0160
    __________________^не фиксированнное количество
    '''
    _url = f'https://api.msrc.microsoft.com/sug/v2.0/en-US/affectedProduct?$orderBy=releaseDate%20desc&$filter=cveNumber%20eq%20%27{CVE}%27'
    with urllib.request.urlopen(_url) as url:
        data = json.load(url)
        return data


def get_best_link(chunk):
    '''
    Отбор лучшей ссылки из строчки в таблице
    Monthly Rollup > Security Update > Security Hotpatch Update
    '''
    links = dict()
    for article in chunk['kbArticles']:
        match article.get('downloadName').lower():
            case 'monthly rollup':
                link = article.get('downloadUrl')
                if link != None:
                    links[2] = link

            case 'security update':
                link = article.get('downloadUrl')
                if link != None:
                    links[1] = link

            case 'security hotpatchd update':
                link = article.get('downloadUrl')
                if link != None:
                    links[0] = link

    if len(links.keys()) == 0:
        raise NoLinkFoundError("No downloadUrl in chunk['kbArticles']")

    return links[max(links.keys())]


def choose(cve: str, platform: str, product: str) -> str:
    '''
    На основе таблицы, платформы и продукта выбирает ссылку
    с лучшим совпадением
    '''
    print("choose")
    # Запрос в апи
    table = get_table(cve)
    # Если таблица пуста, вызываем исключение

    if table['@odata.count'] == 0:
        raise EmptyTableError('No data found on microsoft servers')

    # результаы сравнений
    results = []

    # проход по записям таблицы
    for chunk in table['value']:
        pair = dict()

        # если продукт - ОС, то платформа не содержится в ответе
        if 'platform' in chunk and 'product' in chunk:
            pair['platform'] = compare(chunk['platform'], platform)
            pair['product'] = compare(chunk['product'], product)

        elif 'product' in chunk and 'platform' not in chunk:
            pair['product'] = compare(chunk['product'], product)

        else:
            continue

        # проверка результатов сравнения для каждого элемента пары
        if (0 not in [] if pair.get('platform') == None else pair.get('platform')) and (0 not in pair['product']):
            try:
                link = get_best_link(chunk)
            except NoLinkFoundError:
                link = None

            if link != None:
                res_platform = 0
                if pair.get('platform') != None:
                    res_platform = int(''.join(map(str, pair['platform'])))

                compare_result = int(''.join(map(str, pair['product']))) + res_platform
                # если есть идеальное совпадение - сразу возвращаем результат
                if compare_result == 444 or compare_result == 222:
                    return link
                else:
                    results.append({
                        "link": link,
                        "result": compare_result
                    })

    if len(results) == 0:
        raise NoMatchingLink

    # лучший результат сравнения
    max_result = max([i["result"] for i in results])

    links = []
    for record in results:
        if record["result"] == max_result:
            links.append(record["link"])

    return links[0]


def get_html(updateId):
    _url = main_link + updateId + package_details
    response = requests.get(_url)
    return response.text


def getting_needful_link(url):
    print("getting_needful_link")
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.837 YaBrowser/23.9.4.837 Yowser/2.5 Safari/537.36"
    }

    re = requests.get(url, headers=head)

    textcode = re.text

    soup = BeautifulSoup(textcode, 'lxml')

    count = 0
    all_links = []

    results_background = soup.find(class_='resultsBackGround')
    if results_background:
        table = results_background.find('table')
        if table:
            all_import_lines = table.find_all('tr')

            for item in all_import_lines:
                row = []
                if count != 0:
                    item_id = item.get('id')
                    if item_id:
                        item_id = item_id[:-3]

                        row.append(
                            'https://www.catalog.update.microsoft.com/ScopedViewInline.aspx?updateid=' + str(item_id))
                        words = item.find_all('td')

                        for word in words:
                            row.append(word.text)
                        all_links.append(row)
                count += 1

            final_links = []
            for li in all_links:
                final_links.append([li[0], len(li[3].split(','))])
            max_link = ''
            max_count = 0

            for line in final_links:
                if line[1] > max_count:
                    max_count = line[1]
                    max_link = line[0]
            return max_link

    return None


@lru_cache(maxsize=None)
def find_next_update(updateId: str, cve, po, pl):
    print("process")
    res_html = get_html(updateId)
    res_json = hj.convert(res_html)
    try:
        list_update_changes = \
            res_json.get("html")[0].get("body")[0].get("div")[0].get("form")[1].get("div")[0].get("table")[0].get("tr")[
                0].get(
                "td")[0].get("div")[0].get("div")[0].get("div")[3].get("div")[1].get("div")[0].get("div")[0].get("div")[
                0].get(
                "div")
        if list_update_changes is not None:
            for item in list_update_changes:
                update = item.get("a")[0]
                update_attributes = update.get("_attributes")
                update_href = update_attributes.get("href")
                next_update_id = update_href.split("=")[1]
                # print("обновление", next_update_id)
                find_next_update(next_update_id, cve, po, pl)
        else:
            # cve po pl updateId
            # сохранение в модели CVE этих полей
            updLink = main_link + updateId
            new_cve = Cve(name=cve, platform=pl, product=po, updateLink=updLink)
            new_cve.save()
            print(f"обновление {updLink} самое актуальное для данной CVE")
            return updateId
    except:
        print("ошибка123")


def parse_and_generate_excel(file_path):
    try:
        data = pd.read_excel(file_path)
    except Exception as e:
        return {"error": str(e)}

    try:
        filtered_data = data[['CVE', 'Операционная система', 'Сервис/ПО']]
    except KeyError as e:
        return {"error": f"Столбец {e} не найден"}

    parsed_data = filtered_data.to_dict(orient='records')

    output_file = f'output_{time.strftime("%Y-%m-%d")}.xlsx'
    wb = Workbook()
    ws = wb.active
    ws.append(['CVE', 'Операционная система', 'Сервис/ПО'])

    for row in parsed_data:
        ws.append([row['CVE'], row['Операционная система'], row['Сервис/ПО']])

    wb.save(output_file)
    return output_file


def parse_excel(file_path):
    try:

        data = pd.read_excel(file_path)
    except Exception as e:
        return {"error": str(e)}

    # Оставляем только нужные столбцы
    try:
        filtered_data = data[['CVE', 'Операционная система', 'Сервис/ПО']]
    except KeyError as e:
        return {"error": f"Столбец {e} не найден"}

    parsed_data = filtered_data.to_dict(orient='records')

    return parsed_data


def save_to_excel(request):
    # Получаем данные из базы данных
    data_from_db = Cve.objects.all()

    # Создаем DataFrame на основе данных из базы данных
    data_dict = {
        'CVE': [item.name for item in data_from_db],
        'Product': [item.product for item in data_from_db],
        'Platform': [item.platform for item in data_from_db],
        'Link': [item.updateLink for item in data_from_db],
    }
    df = pd.DataFrame(data_dict)

    # Сохраняем DataFrame в Excel
    output_file = f'output-{time.strftime("%Y-%m-%d")}.xlsx'  # Имя файла для сохранения
    df.to_excel(output_file, index=False)  # Сохраняем данные в Excel без индекса строк

    # Отправляем файл пользователю как ответ на запрос
    with open(output_file, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename={output_file}'
        return response


def process(request):
    if request.method == 'POST':
        file_path = request.POST.get('file_path')

        if file_path is None:
            return HttpResponse("Не хватает данных в запросе")

        result = parse_and_generate_excel(file_path)
        if "error" in result:
            return HttpResponse(result['error'])
        else:
            with open(result, 'rb') as file:
                response = HttpResponse(file.read(), content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = f'attachment; filename={os.path.basename(result)}'
                print(file_path)
                return response
    else:
        return HttpResponse("Этот метод не поддерживается")


def process_file_path(request):
    global user_file_path  # Делаем переменную file_path доступной для изменения

    if request.method == 'POST':
        user_file_path = request.POST.get('file_path')  # Получаем переданный путь к файлу
        # Добавьте вашу логику обработки пути к файлу здесь

        # Пример: вместо этого выводим сообщение в консоль
        print("Путь к файлу:", user_file_path)
        cves = Cve.objects.all()

        for item in cves:
            item.delete()
        func()
        cve_all = Cve.objects.all()
        parse_and_generate_excel(cve_all)
        return render(request, 'index.html', context={'data': cve_all})
    else:
        return JsonResponse({'success': False})  # Ответ о неудачной попытке


def func():
    global user_file_path
    result = parse_excel(user_file_path)
    if "error" in result:
        print(f"Произошла ошибка: {result['error']}")
    else:
        k = 0
        for i, item in enumerate(result[k:len(result)]):
            url1 = ""
            print(i + k, "\n--------\n", item["CVE"],
                  item["Операционная система"],
                  item["Сервис/ПО"]
                  )
            try:
                url1 = choose(
                    item["CVE"],
                    item["Операционная система"],
                    item["Сервис/ПО"]
                )
                print(url1)
            except:
                print("нет данных по kb для этой сve")
            if url1 != "" and "catalog.update.microsoft" in url1:
                updLink = getting_needful_link(url1)
                try:
                    updId = updLink.split("=")[1]
                    print(updLink, updId)
                    find_next_update(updId, item["CVE"], item["Операционная система"], item["Сервис/ПО"])
                except:
                    print("ошибка, save Н/Д")
                    new_cve = Cve(updateLink="Н/Д", platform=item["Операционная система"], name=item["CVE"],
                              product=item["Сервис/ПО"])
                    new_cve.save()
            elif url1 != "" and "www.microsoft.com/download" in url1:
                new_cve = Cve(updateLink=url1, platform=item["Операционная система"], name=item["CVE"],
                              product=item["Сервис/ПО"])
                new_cve.save()
            else:
                new_cve = Cve(updateLink="Н/Д", platform=item["Операционная система"], name=item["CVE"],
                              product=item["Сервис/ПО"])
                new_cve.save()


def index_page(request):
    cve_all = Cve.objects.all()
    parse_and_generate_excel(cve_all)
    return render(request, 'index.html', context={'data': cve_all})
