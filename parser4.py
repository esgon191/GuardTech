import requests, logging
import html_to_json as hj
from sys import setrecursionlimit
from functools import lru_cache
from exceptions import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

FORMAT = "%(asctime)s %(funcName)s %(levelname)s %(message)s"

handler = logging.FileHandler(f"logs/{__name__}.log", mode='a') 
formatter = logging.Formatter(FORMAT)

handler.setFormatter(formatter)
logger.addHandler(handler)

setrecursionlimit(10000)
# основная ссылка, по которой ищутся кбшки
MAIN_LINK = "https://catalog.update.microsoft.com/ScopedView.aspx?updateid="
# якорь на раздел "сведения о пакете"
PACKAGE_DETAILS = "#PackageDetails"


# функция возвращает html по айдишнику апдейта
def get_html(updateId):
    _url = MAIN_LINK + updateId + PACKAGE_DETAILS
    response = requests.get(_url)
    return response.text


# ищет следующую кбшку по айдишнику апдейта
# (P.S. - т.к функция рекуррентная, то она будет долго работать. 
# Чтобы видеть, если я сделал что-то не так (очень сильно в этом сомневаюсь хи-хи), 
# можно раскоментировать принты и проверить работу)
@lru_cache(maxsize=None)
def find_next_update(updateId: str):
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
                logger.info(f"{next_update_id}")
                find_next_update(next_update_id)
        else:
            # cve po pl updateId
            # сохранение в модели CVE этих полей
            updLink = MAIN_LINK + updateId
            #new_cve = Cve(name=cve, platform=pl, product=po, updateLink=updLink)
            #new_cve.save()
            logger.debug(f"обновление {updLink} самое актуальное для данной CVE")
            return updateId
    except:
        raise NextLinkError()        
'''
# рандомные кбшки, можно подставить любую для работы
prev_id1 = "c12328f1-6645-451c-946d-11789665d6b7"
prev_id2 = "257d1360-87fe-4e0f-affe-9ce4fa13de32"
prev_id3 = "72ff447d-fd5d-4fb2-b23a-8e9fcba1a2a2"
find_next_update(prev_id2)
'''
