import datetime
import json
from dotenv import load_dotenv
import os

load_dotenv('.env')


ACTUAL_DATE = datetime.date.today()
TG_TOKEN = os.getenv("TG_TOKEN")


def load_config():
    with open("config.json", "r", encoding="utf-8") as file:
        return json.load(file)

# class Config:
#     USD_RUB = 97.3
#     VON_RUB = 14.9
#     EUR_RUB = 101.2
#
#     DELIVERY_TO_REGION = {"amount": 250000, "currency": "RUB"}
#     BROKER = {"amount": 100000, "currency": "RUB"}
#     OUR_TAX = {"amount": 150000, "currency": "RUB"}
#     KOREAN_EXPENSES = {"amount": 2440000, "currency": "VON"}
#
#     PHYSICAL_UTIL_OLD = {"amount": 5200, "currency": "RUB"}
#     PHYSICAL_UTIL_NEW = {"amount": 3400, "currency": "RUB"}
#
#     LEGAL_UTIL_LT_1000_NEW = {"amount": 180200, "currency": "RUB"}
#     LEGAL_UTIL_1000_2000_NEW = {"amount": 667400, "currency": "RUB"}
#     LEGAL_UTIL_2000_3000_NEW = {"amount": 1875400, "currency": "RUB"}
#
#     LEGAL_UTIL_LT_1000_OLD = {"amount": 460000, "currency": "RUB"}
#     LEGAL_UTIL_1000_2000_OLD = {"amount": 1174000, "currency": "RUB"}
#     LEGAL_UTIL_2000_3000_OLD = {"amount": 2839400, "currency": "RUB"}
#
#     UTIL_GT_3000_FOR_NEW_CAR = {"amount": 2153400, "currency": "RUB"}
#     UTIL_GT_3500_FOR_NEW_CAR = {"amount": 2742200, "currency": "RUB"}
#     UTIL_GT_3000_FOR_OLD_CAR = {"amount": 3296800, "currency": "RUB"}
#     UTIL_GT_3500_FOR_OLD_CAR = {"amount": 3604800, "currency": "RUB"}