from calculator import Calculator
from datetime import date
from logging import getLogger
from parser import ParamsParser
from utils import get_id_from_url
import time

logger = getLogger(__name__)


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        execution_time = end - start
        logger.info(f"Функция {func.__name__} выполнилась за {execution_time:.4f} секунд")
        return result
    return wrapper


@timer
def get_car_price_manual(
    car_price: int,
    car_release_date: date,
    car_engine: int,
    is_electro: bool,
    is_physical_face: bool
):
    total_price = Calculator.calculate_total_price(
        car_von_price=car_price,
        release_date=car_release_date,
        engine=car_engine,
        is_electro=is_electro,
        is_physical_face=is_physical_face
    )
    return total_price


@timer
def get_car_price_auto(url, is_physical_face=True):
    car_id = get_id_from_url(url)
    new_url = f"https://api.encar.com/mobile/search?carIds={car_id}&infinity=1&pageNo=1&searchType=CAR_ID&sort=MOBILE_MODIFIED_DATE"

    parser = ParamsParser(new_url)

    engine_type = parser.is_electric()
    car_price = parser.find_car_von_price()
    car_engine = parser.find_engine()
    car_release_date = parser.find_car_release_date()
    car_image_url = parser.find_image_url()

    total_price = Calculator.calculate_total_price(
        car_von_price=car_price,
        release_date=car_release_date,
        engine=car_engine,
        is_electro=engine_type,
        is_physical_face=is_physical_face
    )
    return total_price, parser.data, car_image_url


