import pandas as pd
from openpyxl import Workbook


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


def generate_excel_from_data(data):
    wb = Workbook()
    ws = wb.active
    ws.append(['CVE', 'Platform', 'Product', 'updateId'])

    for rows in data:
        ws.append([rows['CVE'], rows['Platform'], rows['Product'], rows['updateId']])

    output_file = 'output.xlsx'
    wb.save(output_file)
    return output_file

def func():
    # Пример использования:
    file_path = "C:/Users/artur/Downloads/Эталонный образ RUS сводный.xlsx"  # Укажите путь к загруженному файлу
    
    # Парсинг и фильтрация данных из исходного файла Excel
    result = parse_excel(file_path)
    if "error" in result:
        print(f"Произошла ошибка: {result['error']}")
    else:
        # Создание Excel-файла на основе отфильтрованных данных
        excel_file = generate_excel_from_data(result)
        print(f"Создан Excel-файл: {excel_file}")
    
        # Проверка созданного Excel-файла, чтение и вывод первых строк
        df = pd.read_excel(excel_file)
        return print(df.head())

func()
