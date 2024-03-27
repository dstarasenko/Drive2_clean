import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

from logger import Logger as l
from checks import check_auto, check_Empty

l.start_logs()

# Читаем логин, пароль и исключения из файла Settings.json
try:
    with open('Settings.json', 'r', encoding='utf-8') as json_file:
        l.add_logs(f"Файл 'Settings.json' открыт")
        data = json.load(json_file)
        login = check_Empty(k='login', v=data["login"])
        password = check_Empty(k='password', v=data['password'])
        exception_car = check_Empty(k="exception_cars", v=data['exc_cars'])
        exception_town = check_Empty(k="exception_towns", v=data['exc_towns'])
    json_file.close()
    l.add_logs(f"Файл 'Settings.json' закрыт")
except Exception as e:
    print("Ошибка чтения файла")
    l.add_logs("Ошибка чтения файла Settings.json.")
    sys.exit()

# Настройки драйвера
driver = webdriver.Chrome()
driver.get("https://www.drive2.ru/")
driver.maximize_window()

# Кнопка "Войти", нажимаем
login_btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/header/div/div/div/div[3]/a[1]"))).click()
l.add_logs(f"Кнопка 'Войти' на главной странице нажата")

# Поле логина, вводим логин
login_field = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"loginForm\"]/div[1]/input"))).send_keys(login)
l.add_logs("Логин введен")

# Поле пароля, вводим пароль
password_field = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"loginForm\"]/div[2]/div/input"))).send_keys(password)
l.add_logs("Пароль введен")

# Кнопка "Войти" на странице логина, нажимаем
enter_btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"loginForm\"]/div[4]/div/div[1]/button"))).click()
l.add_logs(f"Кнопка 'Войти' на странице логина нажата")

# Кнопка настроек в виде шестеренки, нажимаем
settings_btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/header/div/div/div/button[2]"))).click()
l.add_logs(f"Кнопка 'Настройки' в виде шестеренки нажата")

# В появившемся меню выбираем пункт "Подписки на машины", нажимаем
car_subscriptions_btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/header/div/div/div/div[1]/a[7]"))).click()
l.add_logs(f"Кнопка 'Подписки на машины' нажата")

# Кол-во машин, на которые подписан пользователь в данный момент
subscribe_counter = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div/div[2]/div[1]/header/h1/span"))).text
l.add_logs(f"Кол-во автомобилей, на которые подписан пользователь в данный момент: {subscribe_counter}")

# Для перемещения к элементу
action = ActionChains(driver)

l.add_logs("Раскрываю страницы")
# Отображаем все подписки: высчитываем кол-во кликов по кнопке "Показать еще" и кликаем.
try:
    for i in range(int(subscribe_counter)//50):
        more_btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='c-block__more']")))
        action.move_to_element(more_btn).perform()
        more_btn.click()
        l.add_logs(f"Кнопка '{more_btn.text}' нажата")
        time.sleep(0.5)
except Exception as e:
    print("Одна страница, кнопка 'Посмотреть ещё' отсутствует")
    l.add_logs("Одна страница, кнопка 'Посмотреть ещё' отсутствует")

# Получаем кол-во "контейнеров" по 50шт, когда все авто будут отображены
arr_car = driver.find_elements(By.XPATH, f"//div[@class='o-grid o-grid--2 o-grid--equal']")
l.add_logs(f"Кол-во страниц\контейнеров по 50 автомобилей: {len(arr_car)}\n-----\n")

# Запускаем функцию проверки автомобиля, записываем возвращаемое значение в переменную
result = check_auto(driver, ec=exception_car, et=exception_town, arr_car=arr_car)

print(f"\n-----\nОтписался от {result} авто\n-----\n")
l.add_logs(f"Отписался от {result} авто")
l.end_logs()
