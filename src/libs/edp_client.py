from selenium import webdriver
from common import selectors
from common.config import log
from common import config
from libs import captcha_client
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from datetime import datetime
from common import utils


class EDPClient:
    def __init__(self, url: str, headless: bool = False) -> None:
        log.info("Iniciando cliente EDP")
        self.driver = webdriver.Chrome()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": config.DONWLOAD_FOLDER,
                "download.prompt_for_download": False,
            },  # Baixar }
        )
        if headless:
            chrome_options.add_argument("--headless")
        self.captcha = captcha_client.CaptchaClient()
        self.driver = webdriver.Chrome(options=chrome_options)
        self.__go_to_url(url)

    def __go_to_url(self, url: str) -> None:
        self.driver.get(url)

    def login(self, username: str, password: str) -> None:
        log.info("Logando no site da EDP")
        log.info("Aceitando cookies")

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, selectors.LOGIN["ACCEPT_COOKIES"])
            )
        ).click()

        log.info("Selecionando a opção 'Para sua casa'")
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, selectors.LOGIN["PARA_SUA_CASA"])
            )
        ).click()

        log.info("Selecionando Estado SP")
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, selectors.LOGIN["ESTADO_SP"]))
        ).click()

        log.info("Preenchendo usuário e senha")
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
            log.info("Quebrando Captch")
            self.driver.execute_script(
                script=f"document.querySelector('textarea#g-recaptcha-response-100000').innerText = '{captcha_response}'"
            )
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, selectors.LOGIN["LOGIN_BTN"]))
        ).click()
        log.info("Login com sucesso")

    def select_instalation(self, instalation: str = "0151129920") -> None:
        log.info(f"Selecionando instalação {instalation}")

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, selectors.INSTALACOES["INST"].format(instalacao=instalation))
            )
        ).click()

    def open_bills(self, instalation: str) -> None:
        log.info(
            "Validando para verificar se a instalação foi selecionada corretamente"
        )
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        selectors.TELA_INSTALACAO["INST_NUMBER"].format(
                            instalacao=instalation
                        ),
                    )
                )
            )
        except TimeoutException:
            log.error("A instalação selecionada não foi a correta")
            raise Exception("Falha ao slecionar instalação")

        log.info("Abrindo Fatura")

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, selectors.TELA_INSTALACAO["BILLS_EXTRACTS"])
            )
        ).click()
        log.info("Navegou para faturas")

    def download_bills(self, dates: list) -> list:
        log.info("Baixando Faturas")
        for date in dates:
            date_parsed = datetime.strptime(date, "%m/%Y")
            month = utils.months_ptbr[date_parsed.month]
            date_str = f"{month}/{date_parsed.year}"
            log.info(f"Selecionando fatura para o mês {date_str}")
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        selectors.SELECT_BILL["BILL_TAB"].replace("{DATA}", date_str),
                    )
                )
            ).click()
            log.info("Abrindo Fatura")
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, selectors.SELECT_BILL["OPEN_BILL"])
                )
            ).click()
            log.info("Baiando Fatura")
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, selectors.SELECT_BILL["DOWNLOAD_BILL"])
                )
            ).click()
            log.info("Fechando Modal")
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, selectors.SELECT_BILL["CLOSE_MODAL"])
                )
            ).click()
            log.info(f"Fatura para o mês {date_str} baixada")

        log.info("Todas as faturas baixadas com sucesso")
        return []
