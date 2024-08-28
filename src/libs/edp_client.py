from selenium import webdriver
from loguru import logger as log
from common import selectors


class EDPClient:
    def __init__(self, url: str, headless: bool = False) -> None:
        log.info("Starting EDP Client...")
        self.driver = webdriver.Chrome()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-extensions")
        if headless:
            chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.__go_to_url(url)

    def __go_to_url(self, url: str) -> None:
        self.driver.get(url)

    def login(self, username: str, password: str) -> None:
        log.info("Logging in to EDP Client")
