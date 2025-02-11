from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton,
                           InlineKeyboardButton,
                           InlineKeyboardMarkup)

# choose_manual_auto_reply = ReplyKeyboardMarkup(keyboard=[
#     [KeyboardButton(text="Автоматически"), KeyboardButton(text="В ручную")]
#     ])

choose_manual_auto_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Автоматически", callback_data="auto"), InlineKeyboardButton(text="Вручную", callback_data="manual")]
], resize_keyboard=True)

repeat_calculation = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Новый расчет", callback_data="new_calc")]
], resize_keyboard=True)

bool_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Да"), KeyboardButton(text="Нет")]
], resize_keyboard=True, one_time_keyboard=True)

engine_type_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Дизель / Бензин"), KeyboardButton(text="Электро")]
], resize_keyboard=True)

manager_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Написать", url="https://wa.me/79185439569")]
])

