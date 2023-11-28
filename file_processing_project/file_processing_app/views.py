import os

import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from openpyxl import Workbook


def index(request):
    return render(request, 'index.html')


def process(request):
    if request.method == 'POST':
        file_path = request.POST['file_path']
        save_path = request.POST['save_path']

        result = parse_and_generate_excel(file_path)
        if "error" in result:
            return HttpResponse(result['error'])
        else:
            with open(result, 'rb') as file:
                response = HttpResponse(file.read(), content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = f'attachment; filename={os.path.basename(result)}'
                print(file_path)
                return response


def parse_and_generate_excel(file_path):
    try:
        data = pd.read_excel(file_path)
    except Exception as e:
        return {"error": str(e)}

    try:
        filtered_data = data[['CVE', 'Platform', 'Product', 'updateId']]
    except KeyError as e:
        return {"error": f"Столбец {e} не найден"}

    parsed_data = filtered_data.to_dict(orient='records')

    output_file = 'output.xlsx'
    wb = Workbook()
    ws = wb.active
    ws.append(['CVE', 'Platform', 'Product', 'updateId'])

    for row in parsed_data:
        ws.append([row['CVE'], row['Platform'], row['Product'], row['updateId']])

    wb.save(output_file)
    return output_file
