from selenium import webdriver
from common import selectors
from common.config import log
from libs import captcha_client
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class EDPClient:
    def __init__(self, url: str, headless: bool = False) -> None:
        log.info("Starting EDP Client...")
        self.driver = webdriver.Chrome()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-extensions")
        if headless:
            chrome_options.add_argument("--headless")
        self.captcha = captcha_client.CaptchaClient()
        self.driver = webdriver.Chrome(options=chrome_options)
        self.__go_to_url(url)

    def __go_to_url(self, url: str) -> None:
        self.driver.get(url)

    def login(self, username: str, password: str) -> None:
        log.info("Logging in to EDP Client")
        log.info("Accepting Cookies")

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, selectors.LOGIN["ACCEPT_COOKIES"])
            )
        ).click()

        log.info("Clicking on 'Para sua casa'")
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, selectors.LOGIN["PARA_SUA_CASA"])
            )
        ).click()

        log.info("Selecting Estado SP")
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, selectors.LOGIN["ESTADO_SP"]))
        ).click()

        log.info("Filling in username and password")
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, selectors.LOGIN["USERNAME"])
            )
        ).send_keys(username)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, selectors.LOGIN["PASSWORD"])
            )
        ).send_keys(password)
        captcha_response = self.captcha.captcha_solver()

        if captcha_response:
            log.info("Filling in captcha")
            self.driver.execute_script(
                script=f"document.querySelector('textarea#g-recaptcha-response-100000').innerText = '{captcha_response}'"
            )
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, selectors.LOGIN["LOGIN_BTN"]))
        ).click()
