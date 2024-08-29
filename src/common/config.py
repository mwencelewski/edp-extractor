from decouple import config
from loguru import logger as log


URL = config("URL")
EMAIL = config("EMAIL")  # Customer Email
PASSWORD = config("PASSWORD")  # Customer Password
SITEKEY = config("SITEKEY")
APIKEY = config("APIKEY")  # 2Captcha API Key
