import re
import requests
from utils import get_id_from_url


class Validator:
    @staticmethod
    def validate_price(param):
        try:
            param = float(param)
            if 1000000 < param < 100000000:
                return True
            return False
        except Exception as e:
            return False

    @staticmethod
    def validate_data(param):
        try:
            month, year = param.split(".")
            month = int(month)
            year = int(year)
            if month in range(1, 13) and year in range(1900, 2026):
                return True
            return False
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def validate_engine(param):
        try:
            param = int(param)
            if 0 <= param < 8000:
                return True
            return False
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def validate_face(param):
        if param.lower() in ("да", "нет"):
            return True
        return False

    @staticmethod
    def is_valid_encar_url(url: str) -> bool:
        pattern = r"^https://fem\.encar\.com/cars/detail/\d+\?.*carid=\d+.*$"
        pattern2 = r"^https://fem\.encar\.com/cars/detail/\d{8}$"
        pattern3 = r"^http://www\.encar\.com/dc/dc_cardetailview\.do\?carid=\d{8}$"
        pattern4 = r"^https://fem\.encar\.com/cars/detail/\d{8}\?.*$"

        try:
            if (
                    bool(re.match(pattern, url)) or
                    bool(re.match(pattern2, url)) or
                    bool(re.match(pattern3, url)) or
                    bool(re.match(pattern4, url))
            ):
                print("тут был")
                id = get_id_from_url(url)
                new_url = f"https://api.encar.com/mobile/search?carIds={id}&infinity=1&pageNo=1&searchType=CAR_ID&sort=MOBILE_MODIFIED_DATE"
                response = requests.get(new_url, verify=False)
                data = response.json()
                try:
                    test = data["general"]["searchResults"][0]["price"]
                    return True
                except Exception as e:
                    return False
            return False
        except Exception as e:
            return False

