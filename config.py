import datetime
import json
from logging import getLogger, StreamHandler, DEBUG, basicConfig
from dotenv import load_dotenv
import os
import colorlog

load_dotenv('.env')


ACTUAL_DATE = datetime.date.today()
TG_TOKEN = os.getenv("TG_TOKEN")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

def load_config():
    with open("config.json", "r", encoding="utf-8") as file:
        return json.load(file)


# -------- logger config --------
formatter = colorlog.ColoredFormatter(
    "%(log_color)s[%(asctime)s] [%(levelname)s] %(message)s",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = getLogger()
handler = StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(DEBUG)
FORMAT = '%(asctime)s : %(name)s : %(levelname)s : %(message)s'
basicConfig(level=DEBUG, format=FORMAT)