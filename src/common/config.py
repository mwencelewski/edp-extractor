from decouple import config
from loguru import logger as log
from datetime import datetime
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = config("URL")
EMAIL = config("EMAIL")  # Customer Email
PASSWORD = config("PASSWORD")  # Customer Password
SITEKEY = config("SITEKEY")
APIKEY = config("APIKEY")  # 2Captcha API Key


DONWLOAD_FOLDER = os.path.join(ROOT, "downloads")
LOGS = os.path.join(ROOT, "logs")

log.add(
    os.path.join(LOGS, f"{datetime.strftime(datetime.now(),'%d-%m-%y-%h-%m-%s')}.log")
)
