import requests
import os
from bs4 import BeautifulSoup

""" ПАРСИНГ КУРСА ЕВРО """
def get_eur_CB():  # Курс евро в ЦБ
    url = "https://www.banki.ru/products/currency/eur/"
    request_ = requests.get(url)
    if request_.status_code == 200:
        soup = BeautifulSoup(request_.text, "html.parser")
        eur = soup.findAll('div', class_='currency-table__large-text')
        return float(eur[2].text.replace(",", "."))
    else:
        print("Страница не найдена")

def get_eur_Sber():  # Курс евро в Сбер
    url = "https://www.banki.ru/products/currency/bank/sberbank/moskva/"
    request_ = requests.get(url)
    if request_.status_code == 200:
        soup = BeautifulSoup(request_.text, "html.parser")
        eur = soup.findAll('td', class_='font-size-large')
        return eur[3].text[8:13].replace(",", ".")
    else:
        print("Страница не найдена")

def get_eur_Tinkoff():  # Курс евро в Тинькофф
    url = "https://ru.myfin.by/bank/tcs/currency"
    request_ = requests.get(url)
    if request_.status_code == 200:
        soup = BeautifulSoup(request_.text, "html.parser")
        eur = soup.findAll('table', class_='table-best white_bg')
        return eur[0].findAll('td')[7].text.replace(",", ".")

    else:
        print("Страница не найдена")

""" КОНСТАНТЫ """
TOKEN = os.environ.get('BOT_TOKEN')

nike_size = 'photo-188973350_457239023'
admin_id = None
load_photo = False


