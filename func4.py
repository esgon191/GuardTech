import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

KB_number_from_func3 = input("Введите номер KB: ") # KB4016871 для примера
search_url = f'https://catalog.update.microsoft.com/Search.aspx?q={KB_number_from_func3}'

# Используйте webdriver.Chrome() без аргументов
driver = webdriver.Chrome()

driver.get(search_url)

# Находим кнопку "Загрузить" по тексту на кнопке
download_button = driver.find_element(By.XPATH, "//input[@value='Загрузить']")
download_button.click()

# Ожидаем нового окна браузера
new_window = driver.window_handles[1]
driver.switch_to.window(new_window)

# Выполняем JavaScript-код для получения ссылки
download_url = driver.execute_script("return downloadInformation[0].files[0].url")

# Создаем строку с ссылкой
link = download_url

# Возвращаем ссылку
print(f"Cсылка на обновление: {link}")

driver.quit()





