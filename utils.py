import asyncio
from urllib.parse import urlparse, parse_qs
import re
import aiohttp
import json


API_URL = "https://www.cbr-xml-daily.ru/daily_json.js"


def get_id_from_url(url):
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)
    carid = params.get("carid", [None])[0]

    if carid is None:
        match = re.search(r"/cars/detail/(\d{8})", parsed_url.path)
        if match:
            carid = match.group(1)
    return carid


async def get_exchange_rate():
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as response:
            data = await response.text()
            json_data = json.loads(data)
            USD_RUB = json_data["Valute"]["USD"]["Value"]
            VON_RUB = 1000/json_data["Valute"]["KRW"]["Value"]
            EUR_RUB = json_data["Valute"]["EUR"]["Value"]

            return {
                "USD_RUB": USD_RUB,
                "VON_RUB": VON_RUB,
                "EUR_RUB": EUR_RUB
            }



