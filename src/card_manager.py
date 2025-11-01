import flet as app
from pydantic import BaseModel
import json
import os

from models.card import Card

DATA_PATH = os.getenv("FLET_APP_STORAGE_DATA")

class Card_Model(BaseModel):
    service: str
    login: str
    password: str

CARDS_LIST = [Card_Model(service="mail", login="2mlogin", password="12345"), Card_Model(service="google", login="3mlogin", password="12345")]
FILTRATED_CARDS_LIST = []


# def get():
#     tmp = into_card()
#     cards = tmp[0]
#     fcards = tmp[1]



def load():
    path = f"{DATA_PATH}/data.json"
    cards = []

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    for i in data:
        cards.append(Card_Model(**i))

    CARDS_LIST = cards


def save(data: list[Card_Model]):
    path = f"{DATA_PATH}/data.json"

    with open(path, "w", encoding="utf-8") as file:
        json.dump([f.model_dump() for f in data], file, indent=4, ensure_ascii=False)


def filter_card(key: str):
    global CARDS_LIST, FILTRATED_CARDS_LIST
    key = key.strip()

    if len(key) < 3: return

    def s(c):
        login = c.login
        service = c.service
        if key in login or key in service:
            return True
        else: return False

    result = list(filter(s, CARDS_LIST))
    FILTRATED_CARDS_LIST = result

    return result


def get_in_card():
    print("ты в гет")
    cards = []
    fcards = []
    print(CARDS_LIST, FILTRATED_CARDS_LIST)
    for i in CARDS_LIST:
        cards.append(Card(service_name=i.service, login=i.login))
    
    for i in FILTRATED_CARDS_LIST:
        fcards.append(Card(service_name=i.service, login=i.login))
    
    return (cards, fcards)


def add_card():
    ...


def remove_card():
    ...


