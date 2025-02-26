from config import load_config, ACTUAL_DATE
from datetime import date
from utils import get_exchange_rate


class Calculator:
    @staticmethod
    def calculate_car_age(car_release_date, current_date=ACTUAL_DATE):
        """
        Считает промежуток с 3 до 5 лет
        """
        car_age = (current_date.year - car_release_date.year) - (
                (current_date.month, current_date.day) < (car_release_date.month, car_release_date.day)
        )

        # Определяем категорию
        if 3 <= car_age < 5:
            return "3_to_5"
        elif car_age < 3:
            return "lt_3"
        else:
            return "gt_5"

    @staticmethod
    async def convert_to_rub(dict_):
        """
        конвертирует воны, доллары и евро в рубли
        """
        config = load_config()

        if config["MODE"] == "AUTO":
            currency = await get_exchange_rate()
        else:
            currency = config

        if dict_["currency"] == 'USD':
            return {"amount": dict_["amount"] * currency["USD_RUB"], "currency": "RUB"}
        elif dict_["currency"] == 'EUR':
            return {"amount": dict_["amount"] * currency["EUR_RUB"], "currency": "RUB"}
        elif dict_["currency"] == 'VON':
            return {"amount": dict_["amount"] / currency["VON_RUB"], "currency": "RUB"}
        else:
            raise ValueError("Unsupported currency")

    @staticmethod
    async def calculate_tax(release_date, engine, car_rub_price):
        """
        считает сумму налога
        """
        config = load_config()

        car_age = Calculator.calculate_car_age(release_date)
        if car_age == '3_to_5':
            if engine < 1000:
                tax = engine * 1.5
            elif 1000 <= engine < 1500:
                tax = engine * 1.7
            elif 1500 <= engine < 1800:
                tax = engine * 2.5
            elif 1800 <= engine < 2300:
                tax = engine * 2.7
            elif 2300 <= engine <= 3000:
                tax = engine * 3
            else:
                tax = engine * 3.6
            tax_rub = await Calculator.convert_to_rub({"amount": tax, "currency": "EUR"})
            return tax_rub
        elif car_age == 'lt_3':
            car_price_eur = car_rub_price["amount"] / config["EUR_RUB"]

            car_price_eur_48 = car_price_eur * 0.48

            if car_price_eur <= 8500:
                car_price_eur_54 = car_price_eur * 0.54
                price_engine = engine * 2.5
                if price_engine > car_price_eur_54:
                    tax = await Calculator.convert_to_rub({"amount": price_engine, "currency": "EUR"})
                    return tax
                else:
                    tax = await Calculator.convert_to_rub({"amount": car_price_eur_54, "currency": "EUR"})
                    return tax
            elif 8501 <= car_price_eur <= 16700:
                price_engine = engine * 3.5
            elif 16701 <= car_price_eur <= 42300:
                price_engine = engine * 5.5
            elif 42301 <= car_price_eur <= 84500:
                price_engine = engine * 7.5
            elif 84501 <= car_price_eur <= 169000:
                price_engine = engine * 15
            else:
                price_engine = engine * 20
            if price_engine > car_price_eur_48:
                tax = await Calculator.convert_to_rub({"amount": price_engine, "currency": "EUR"})
                return tax
            else:
                tax = await Calculator.convert_to_rub({"amount": car_price_eur_48, "currency": "EUR"})
                return tax
        else:
            print("мы не валидируем машины старше 5 лет")
            return {"amount": 0, "currency": "RUB"}

    @staticmethod
    def calculate_tax_electro(car_rub_price):
        tax = car_rub_price["amount"]*0.39
        return {"amount": tax, "currency": "RUB"}

    @staticmethod
    def calculate_util(
            car_release_date: date,
            engine: int,
            is_physical_face: bool,
            current_date: date = ACTUAL_DATE
    ) -> int:
        config = load_config()

        car_age = (current_date.year - car_release_date.year) - (
                (current_date.month, current_date.day) < (car_release_date.month, car_release_date.day))
        older_than_3_years = car_age >= 3

        if is_physical_face:
            if engine <= 3000:
                return config["PHYSICAL_UTIL_OLD"] if older_than_3_years else config["PHYSICAL_UTIL_NEW"]
            elif 3000 < engine < 3500:
                return config["UTIL_GT_3000_FOR_OLD_CAR"] if older_than_3_years else config["UTIL_GT_3000_FOR_NEW_CAR"]
            else:
                return config["UTIL_GT_3500_FOR_OLD_CAR"] if older_than_3_years else config["UTIL_GT_3500_FOR_NEW_CAR"]

        if engine < 1000:
            return config["LEGAL_UTIL_LT_1000_OLD"] if older_than_3_years else config["LEGAL_UTIL_LT_1000_NEW"]
        elif 1000 <= engine < 2000:
            return config["LEGAL_UTIL_1000_2000_OLD"] if older_than_3_years else config["LEGAL_UTIL_1000_2000_NEW"]
        elif 2000 <= engine <= 3000:
            return config["LEGAL_UTIL_2000_3000_OLD"] if older_than_3_years else config["LEGAL_UTIL_2000_3000_NEW"]
        elif 3000 < engine < 3500:
            return config["UTIL_GT_3000_FOR_OLD_CAR"] if older_than_3_years else config["UTIL_GT_3000_FOR_NEW_CAR"]
        else:
            return config["UTIL_GT_3500_FOR_OLD_CAR"] if older_than_3_years else config["UTIL_GT_3500_FOR_NEW_CAR"]

    @staticmethod
    async def calculate_total_price(car_von_price, release_date, engine, is_electro, is_physical_face=True):
        print("Считаю стоимость авто!")
        config = load_config()
        try:
            car_rub_price = await Calculator.convert_to_rub({"amount": car_von_price, "currency": "VON"})
            if is_electro:
                tax_price = Calculator.calculate_tax_electro(car_rub_price)
            else:
                tax_price = await Calculator.calculate_tax(release_date, engine, car_rub_price)
            if tax_price["amount"] == 0:
                return None
            util_price = Calculator.calculate_util(release_date, engine, is_physical_face)
            korean_expenses_to_rub = await Calculator.convert_to_rub({
                "amount": config["KOREAN_EXPENSES"]["amount"],
                "currency": config["KOREAN_EXPENSES"]["currency"]
            })

            total_price_rub = sum(
                [
                    car_rub_price["amount"],
                    tax_price["amount"],
                    util_price["amount"],
                    korean_expenses_to_rub["amount"],
                    # config["DELIVERY_TO_REGION"]["amount"],
                    config["BROKER"]["amount"],
                    config["OUR_TAX"]["amount"]
                ]
            )
            return {
               "price": round(total_price_rub),
                "car_rub_price": round(car_rub_price["amount"]),
                "tax_price": round(tax_price["amount"]),
                "util_price": round(util_price["amount"]),
                "korean_expenses": round(korean_expenses_to_rub["amount"]),
                "delivery_to_region": round(config["DELIVERY_TO_REGION"]["amount"]),
                "broker": round(config["BROKER"]["amount"]),
                "our_tax": round(config["OUR_TAX"]["amount"])

            }
        except Exception as e:
            print(e)
            print("ошибка в функции calculate_total_price")
            return None
