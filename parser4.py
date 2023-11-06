import requests
import html_to_json as hj
from sys import setrecursionlimit
from functools import lru_cache


setrecursionlimit(10000)
# основная ссылка, по которой ищутся кбшки
main_link = "https://catalog.update.microsoft.com/ScopedView.aspx?updateid="
# якорь на раздел "сведения о пакете"
package_details = "#PackageDetails"


# функция возвращает html по айдишнику апдейта
def get_html(updateId):
    _url = main_link + updateId + package_details
    response = requests.get(_url)
    return response.text


# ищет следующую кбшку по айдишнику апдейта
# (P.S. - т.к функция рекуррентная, то она будет долго работать. Чтобы видеть, если я сделал что-то не так (очень сильно в этом сомневаюсь хи-хи), можно раскоментировать принты и проверить работу)
@lru_cache(maxsize=None)
def find_next_update(updateId):
    # получает html по айдишнику апдейта
    res_html = get_html(updateId)
    # конвертирует html строку в json
    res_json = hj.convert(res_html)
    # тут я сам хз как это сделал, но в итоге получается массив из тегов обновлений
    list_update_changes = \
        res_json.get("html")[0].get("body")[0].get("div")[0].get("form")[1].get("div")[0].get("table")[0].get("tr")[
            0].get(
            "td")[0].get("div")[0].get("div")[0].get("div")[3].get("div")[1].get("div")[0].get("div")[0].get("div")[
            0].get(
            "div")
    # когда массив обновлений пустой, то есть Н/Д, то он None, поэтому проверяем его на None, чтобы он работал дальше
    if list_update_changes is not None:
        # перебираем каждый айтем в массиве
        for item in list_update_changes:
            # получаем сам апдейт
            update = item.get("a")[0]
            # аттрибуты - это ссылка на следующую кбшку
            update_attributes = update.get("_attributes")
            # забираем эту ссылку
            update_href = update_attributes.get("href")
            # берем айдишник на кбшку в конце ссылки
            next_update_id = update_href[25:]

            # это имя обновления (на всякий случай)
            #update_value = update.get("_value")
            # это для отладки, чтобы видеть, какие кбшки он проходит
            #print("обновление", next_update_id, update_value)

            # ну и начинаем работу рекурсии: функция будет вызывать сама себя и работать, пока не обнаружит Н/Д (None) в списке апдйетов
            find_next_update(next_update_id)
    else:
        # если массив Н/Д (None), то завершаем работу функции
        # переданный в последний вызов updateId и есть самое актуальное обновление, которое нам нужно
        print(f"обновление {updateId} самое актуальное для данной CVE")
        return type(updateId), updateId


# рандомные кбшки, можно подставить любую для работы
prev_id1 = "c12328f1-6645-451c-946d-11789665d6b7"
prev_id2 = "257d1360-87fe-4e0f-affe-9ce4fa13de32"
prev_id3 = "72ff447d-fd5d-4fb2-b23a-8e9fcba1a2a2"
find_next_update(prev_id2)
