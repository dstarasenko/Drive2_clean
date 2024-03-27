import sys

from logger import Logger as l
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""
    Основная функция проверки автомобиля на соответствие фильтрам.
    
    Получает:
    driver - драйвер Chrome'a
    ec - список автомобилей, которые нужно оставить в подписках
    et - список городов, которые нужно оставить в подписках
    arr_car - кол-во "контейнеров" по 50шт, когда все авто будут отображены
"""
# Счетчики отписок и кол-ва проверенных авто
count_unsubscribe = 0
count_cars = 0
def check_auto(driver, ec, et, arr_car):
    action = ActionChains(driver)

    try:
        global count_unsubscribe    # Счетчик для отписанных авто
        global count_cars           # Счетчик для всех авто(итераций)

        l.add_logs("Начинаю проверку автомобилей на соответствие фильтру")

        # По каждой странице(контейнеру)
        for el in range(1, len(arr_car)+1):
            # Кол-во машин на странице
            count_el = driver.find_elements(By.XPATH, f"//*[@class='o-grid o-grid--2 o-grid--equal'][{el}]/div")
            l.add_logs(f"Кол-во машин на странице: {len(count_el)}")
            # По каждой машине на странице
            for n in range(1, len(count_el)+1):
                count_cars += 1
                check = {"car": False, "town": False}
                # Марка + модель авто
                car_label = driver.find_element(By.XPATH,f"//*[@class='o-grid o-grid--2 o-grid--equal'][{el}]/div[{n}]/div[2]/span")
                # Город авто
                town_label = driver.find_element(By.XPATH,f"//*[@class='o-grid o-grid--2 o-grid--equal'][{el}]/div[{n}]/div[3]/div[2]/span")
                action.move_to_element(town_label).perform()
                link = driver.find_element(By.XPATH, f"/html/body/main/div/div[2]/div[2]/div[1]/div/div[{el}]/div[{n}]/a").get_attribute('href')
                txt_subs = driver.find_element(By.XPATH, f"//*[@class='c-car-card-sa c-darkening-hover-container c-car-card-sa--2nd'][{n}]/div/div/div/button").text
                # Вывод информации о проверяемом авто
                print(f"{count_cars}: {car_label.text}, {town_label.text}, Ссылка: {link}")
                l.add_logs(f"{count_cars}: {car_label.text}, {town_label.text}, Ссылка: {link}")

                # Проверка есть ли текущий авто в исключениях
                for car in ec:
                    if car.lower() in car_label.text.lower():
                        #print("Авто совпало")
                        l.add_logs("Есть совпадение по авто")
                        check["car"] = True
                        break

                # Проверка есть ли текущий город в исключениях
                for town in et:
                    if town.lower() in town_label.text.lower():
                        #print("Город совпал")
                        l.add_logs("Есть совпадение по городу")
                        check["town"] = True
                        break

                #print(check)
                l.add_logs(f"Результат проверки: {str(check)}")

                # Если автомобиль и город отсутствуют в исключениях, то запускается процесс отписки
                if check['car'] is False and check['town'] is False and txt_subs == "Читаю":
                    # Такая конструкция понадобилась чтобы избежать ошибки
                    button_subscribe = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, f"//*[@class='c-car-card-sa c-darkening-hover-container c-car-card-sa--2nd'][{n}]/div/div/div/button")))
                    driver.execute_script("arguments[0].click();", button_subscribe)

                    button_unsubscribe = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, f"/html/body/div[2]/div/div[2]/div/button[1]")))
                    driver.execute_script("arguments[0].click();", button_unsubscribe)

                    print("----- Нет совпадений. Отписался. -----")
                    l.add_logs("Нет совпадений. Отписался.")
                    time.sleep(0.5)
                    count_unsubscribe += 1

                l.add_logs(f"-----")
    except Exception as e:
        print(e)

    # Возвращаем кол-во машин, от которых отписались
    return count_unsubscribe


# Проверка на пустые поля в файле Settings.json
def check_Empty(k, v):
    if (type(v) is str and v == "") or (type(v) is list and len(v) == 0):
        #print(f"Поле {k} пустое, необходимо заполнить его в файле Settings.json")
        l.add_logs(f"Поле {k} пустое, необходимо заполнить его в файле Settings.json")
        l.end_logs()
        sys.exit()
    else:
        l.add_logs(f"Поле {k} заполнено")
        return v