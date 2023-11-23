import pandas as pd


def parse_excel(file_path):
    # Чтение Excel-файла
    try:
        data = pd.read_excel(file_path)  # Загрузка данных из файла
    except Exception as e:
        return {"error": str(e)}

    # Оставляем только нужные столбцы
    try:
        filtered_data = data[['CVE', 'Platform', 'Product', 'updateId']]
    except KeyError as e:
        return {"error": f"Столбец {e} не найден"}

    # Преобразование данных в формат списка словарей для передачи на бэкенд
    parsed_data = filtered_data.to_dict(orient='records')

    return parsed_data


# Пример использования:
file_path = "C:/Users/artur/Downloads/Эталонный образ RUS сводный.xlsx"  # Укажите путь к загруженному файлу

result = parse_excel(file_path)
if "error" in result:
    print(f"Произошла ошибка: {result['error']}")
else:
    for row in result:
        print(row)
