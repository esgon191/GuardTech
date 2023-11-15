import re
from clear import format_api, format_local

def markup(product: str) -> dict:
    '''
    Размечает строку по шаблону для дальнейшего сравнения.
    Позволяет определить, что за продукт перед нами.
    '''

    #дальнейшие функции проверяют принадлежность
    #слова из продукта к какому-то из атрибутов
    def is_razr(atribute: str) -> bool:
        #является ли разрядностью
        reg = r'^(x|arm)*(32|64)(-based|-bit)?$'

        if re.fullmatch(reg, atribute) != None:
            match = re.fullmatch(reg, atribute)[0]
            if 'arm' in match:
                return 'arm'+''.join([i for i in match if i.isdigit()])
            
            else:
                return ''.join([i for i in match if i.isdigit()])

    def is_version(atribute: str) -> bool:
        #является ли версией
        reg = r'^([0-9]+\.)[0-9+](.[0-9])*'

        if re.fullmatch(reg, atribute) != None:
            return re.fullmatch(reg, atribute)[0]


    marked_up = {
        'keywords' : [], #ключевые слова
        'versions' : [], #список списков версий, промежутков версий продукта
        'razr' : None, #разрядность
    }

    product = product.split(' ')
    to_skip = 0

    for i in range(len(product)):
        if to_skip > 0:
            to_skip -= 1
            continue 

        if product[i] == 'includes':
            marked_up['versions'].append((product[i+1], product[i+3]))
            to_skip = 3
      
        elif is_razr(product[i]) != None:
            marked_up['razr'] = is_razr(product[i])

        elif is_version(product[i]) != None:
            marked_up['versions'].append(is_version((product[i])))

        else:
            marked_up['keywords'].append(product[i])

    marked_up['keywords'].sort()

    return marked_up


def rate_match(atr_local: (list | str), atr_api: (list | str), type_of_atr: str) -> int:
    '''
    Оценивает насколько совпадает передаваемые атрибуты
    Возвращает Число от 0 до 2
    '''
    match type_of_atr:
        case 'keywords':
            if atr_api == atr_local:
                return 2

            else:
                flag = True
                for i in range(min(len(atr_api), len(atr_local))):
                    if atr_api[i] != atr_local[i]:
                        flag = False

                if flag:
                    return 1

                return 0

        case 'versions':
            if len(atr_api) == 0 and len(atr_local) == 0:
                return 2

            for version in atr_api:
                match version:
                    case str():
                        if atr_local[0] == version:
                            return 2

                    case tuple():
                        def format_version(v):
                            #"16.2.8" -> [16, 2, 8]
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
        print(product_api, product_local, key)
        rating.append(rate_match(product_local[key], product_api[key], key))

    return rating















