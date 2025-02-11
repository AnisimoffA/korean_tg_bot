import requests
import urllib3
import json
import re
from datetime import datetime, date

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
url = "https://api.encar.com/mobile/search?carIds=38966743&infinity=1&pageNo=1&searchType=CAR_ID&sort=MOBILE_MODIFIED_DATE"
url2 = "https://api.encar.com/v1/readside/record/vehicle/38572560/summary"


class ParamsParser:
    def __init__(self, url):
        response = requests.get(url, verify=False)
        self.data = response.json()

    def find_id_for_engine(self):
        id_for_engine = self.data["general"]["searchResults"][0]["photos"][0]["location"]

        match = re.search(r"/(\d+)_", id_for_engine)
        if match:
            number = match.group(1)
            return number
        else:
            return None

    def find_image_url(self):
        image_path = self.data["general"]["searchResults"][0]["photos"][0]["location"]
        return "https://ci.encar.com" + image_path

    def find_car_von_price(self) -> int:
        price = str(self.data["general"]["searchResults"][0]["price"])
        price += "0000"
        return int(price)

    def find_car_release_date(self) -> date:
        release_date = str(self.data["general"]["searchResults"][0]["year"])
        year, month = int(release_date[:4]), int(release_date[4:])
        car_release_date = date(year, month, 1)
        return car_release_date

    def find_engine(self) -> int:
        id_for_engine = self.find_id_for_engine()

        url = f"https://api.encar.com/v1/readside/record/vehicle/{id_for_engine}/summary"
        response = requests.get(url, verify=False)
        data = response.json()

        engine = int(data["displacement"])
        return engine

    def is_electric(self):
        engine_type = self.data["general"]["searchResults"][0]["fuelType"]
        if engine_type == "전기":
            return True
        return False



