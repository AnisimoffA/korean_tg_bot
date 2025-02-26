import json
from datetime import date
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, URLInputFile
from aiogram import F, Router
import telegram.keyboards as kb
from aiogram.fsm.context import FSMContext
from telegram.states import InsertURL, CarInfo
from utils import get_exchange_rate
from validator import Validator
from main import get_car_price_auto, get_car_price_manual
from telegram.templates.price_answer import (get_price_answer_auto,
                                             get_price_answer_manual,
                                             get_hello_message)
import logging

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        text=get_hello_message(),
        reply_markup=kb.choose_manual_auto_inline,
        parse_mode=ParseMode.HTML
    )


@router.callback_query(F.data == "new_calc")
async def new_calc(callback: CallbackQuery):
    await callback.message.answer( "Выберите вариант рассчета:", reply_markup=kb.choose_manual_auto_inline)


@router.message(Command('set_config'))
async def set_config(message: Message):
    """
    функция для смены значений конфига
    """
    if message.from_user.id not in [217120905, 1718742365]:
        await message.answer(text=f"Доступ запрещен. Ваш ID - {message.from_user.id}")
    else:
        try:
            _, key, value = message.text.split(maxsplit=2)

            with open("config.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            if key.upper() in data:
                if key.upper() == "MODE":
                    if value.upper() in ["AUTO", "MANUAL"]:
                        data[key.upper()] = str(value).upper()
                        logging.debug(f"Мод изменен на {data[key.upper()]}")
                    else:
                        raise Exception("мод может быть либо AUTO, либо MANUAL")
                elif key.upper() in ["USD_RUB", "VON_RUB", "EUR_RUB"]:
                    data[key.upper()] = float(value)
                    logging.debug(f"Курс {key.upper()} изменен на {value}")
                elif key.upper() in ["KOREAN_EXPENSES"]:
                    new_value = {"amount": int(value), "currency": "VON"}
                    data[key.upper()] = new_value
                    logging.debug(f"Расходы по Корее изменены на {value}")
                else:
                    new_value = {"amount": int(value), "currency": "RUB"}
                    data[key.upper()] = new_value
            else:
                raise Exception(f"Такого ключа не существует")

            with open("config.json", "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            await message.answer("Значение успешно записано")

        except Exception as e:
            await message.answer(text=f"Ошибка: {e}")


@router.message(Command('get_currency'))
async def set_config(message: Message):
    """
    Команда для получения курса с внешнего апи
    """
    if message.from_user.id not in [217120905, 1718742365]:
        await message.answer(text=f"Доступ запрещен. Ваш ID - {message.from_user.id}")
    else:
        data = await get_exchange_rate()
        output = "\n".join(f"{key}: {round(value, 2)}" for key, value in data.items())

        await message.answer(output)


@router.message(Command('config'))
async def set_config(message: Message):
    """
    Команда для получения конфига
    """
    if message.from_user.id not in [217120905, 1718742365]:
        await message.answer(text=f"Доступ запрещен. Ваш ID - {message.from_user.id}")
    else:
        with open("config.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        output = []
        for key, value in data.items():
            if key.upper() == "LEGAL_UTIL_LT_1000_NEW":
                break
            if isinstance(value, dict):
                output.append(f"{key}: {value['amount']} {value['currency']}")
            else:
                output.append(f"{key}: {value}")

        await message.answer("\n".join(output))


# -------------------------------- MANUAL ---------------------------------------
@router.callback_query(F.data == "manual")
async def manual(callback: CallbackQuery, state: FSMContext):
    await state.set_state(CarInfo.car_von_price)
    await callback.message.answer("Введите цену в вонах: ")


@router.message(CarInfo.car_von_price)
async def car_von_price(message: Message, state: FSMContext):
    await state.update_data(car_von_price=message.text)

    data = await state.get_data()

    if Validator.validate_price(data["car_von_price"]):
        price = int(data["car_von_price"])
        await state.update_data(car_von_price=price)

        await state.set_state(CarInfo.release_date)
        await message.answer("Введите дату производства в формате ММ.ГГГГ: ")
    else:
        await message.answer("Введите цену корректно. Возможно, она слишком низкая: ")


@router.message(CarInfo.release_date)
async def release_date(message: Message, state: FSMContext):
    await state.update_data(release_date=message.text)

    data = await state.get_data()

    if Validator.validate_data(data["release_date"]):
        month, year = data["release_date"].split(".")
        month = int(month)
        year = int(year)
        car_release_date = date(year, month, 1)
        await state.update_data(release_date=car_release_date)

        await state.set_state(CarInfo.engine)
        await message.answer("Введите объем двигателя в см3 (для электромобилей - 0): ")
    else:
        await message.answer("Введите дату корректно: ")


@router.message(CarInfo.engine)
async def engine(message: Message, state: FSMContext):
    await state.update_data(engine=message.text)

    data = await state.get_data()

    if Validator.validate_engine(data["engine"]):
        car_engine = int(data["engine"])
        await state.update_data(engine=car_engine)

        await state.set_state(CarInfo.is_electro)
        await message.answer("Выберите тип двигателя: ", reply_markup=kb.engine_type_kb)

    else:
        await message.answer("Введите объем двигателя корректно: ")


@router.message(CarInfo.is_electro)
async def is_electro(message: Message, state: FSMContext):
    await state.update_data(is_electro=message.text)

    data = await state.get_data()

    if data["is_electro"].lower() == "электро":
        await state.update_data(is_electro=True)
    else:
        await state.update_data(is_electro=False)

    await state.set_state(CarInfo.is_physical_face)
    await message.answer("Машина таможится на физическое лицо?", reply_markup=kb.bool_kb)


@router.message(CarInfo.is_physical_face)
async def is_physical_face(message: Message, state: FSMContext):
    await state.update_data(is_physical_face=message.text)

    data = await state.get_data()

    if data["is_physical_face"].lower() == "да":
        face = True
        await state.update_data(is_physical_face=face)
        await state.clear()

        price_info = await get_car_price_manual(
            car_price=data["car_von_price"],
            car_release_date=data["release_date"],
            car_engine=data["engine"],
            is_electro=data["is_electro"],
            is_physical_face=data["is_physical_face"]
        )

        if price_info:
            await message.answer(
                text=get_price_answer_manual(price_info),
                parse_mode=ParseMode.HTML,
                reply_markup=kb.repeat_calculation)
        else:
            await message.answer(f"Мы не работаем с машинами старше 5 лет", reply_markup=kb.repeat_calculation)

    elif data["is_physical_face"].lower() == "нет":
        await message.answer(f"""Рассчеты для юридических лиц сложнее и проводятся менеджером компании Романом. Вы можете написать ему лично""", reply_markup=kb.manager_kb)
        face = False
        await state.update_data(is_physical_face=face)
        await state.clear()


# -------------------------------- AUTO ---------------------------------------
@router.callback_query(F.data == "auto")
async def auto(callback: CallbackQuery, state: FSMContext):
    await state.set_state(InsertURL.url)
    await callback.message.answer("Введите URL: ")


@router.message(InsertURL.url)
async def url(message: Message, state: FSMContext):
    await state.update_data(url=message.text)
    await state.set_state(InsertURL.url)

    data = await state.get_data()

    if Validator.is_valid_encar_url(data["url"]):
        await state.clear()

        price_info, http_response_json, image_url = await get_car_price_auto(data["url"])

        if price_info:
            await message.answer_photo(
                URLInputFile(image_url),
                caption=get_price_answer_auto(price_info, http_response_json),
                parse_mode=ParseMode.HTML,
                reply_markup=kb.repeat_calculation
            )

        else:
            await message.answer(f"Мы не работаем с машинами старше 5 лет", reply_markup=kb.repeat_calculation)

    else:
        await message.answer("Некорректный URL. Пожалуйста, введите еще раз:")
