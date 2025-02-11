from aiogram.fsm.state import State, StatesGroup


class InsertURL(StatesGroup):
    url = State()


class CarInfo(StatesGroup):
    car_von_price = State()
    release_date = State()
    engine = State()
    is_electro = State()
    is_physical_face = State()