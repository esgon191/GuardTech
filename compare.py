import re

def markup(product: str) -> dict:
    '''
    Размечает строку по шаблону для дальнейшего сравнения.
    Позволяет определить, что за продукт перед нами.
    '''

    #дальнейшие функции проверяют принадлежность
    #слова из продукта к какому-то из атрибутов
    def is_razr(atribute: str) -> bool:
        #является ли разрядностью
        reg = r'^[x]*(32|64)(-based|-bit)?$'

        if re.fullmatch(reg, atribute) != None:
            return ''.join([i for i in re.fullmatch(reg, atribute)[0] if i.isdigit()])

    def is_version(atribute: str) -> bool:
        #является ли версией
        reg = r'^([0-9]+\.)[0-9+](.[0-9])*'

        if re.fullmatch(reg, atribute) != None:
            return re.fullmatch(reg, atribute)[0]


    marked_up = {
        'keywords' : [],
        'version' : None,
        'razr' : None
    }

    product = product.split(' ')

    for word in product:
        if is_razr(word) != None:
            marked_up['razr'] = is_razr(word)

        elif is_version(word) != None:
            marked_up['version'] = is_version(word)

        else:
            marked_up['keywords'].append(word)


    return marked_up

def compare(product_api: str, product_local: str) -> bool:
    '''
    Устанавливает, являются ли две строки разными
    названиями одного продукта
    '''

    product_local = format_local(product_local)
    product_api = format_api(product_api)

    product_local = markup(product_local)
    product_api = markup(product_api)