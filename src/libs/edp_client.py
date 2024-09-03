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
import os


class EDPClient:

    """
    EDPClient é um cliente de automação web projetado para interagir com o portal da EDP (Distribuição de Energia Elétrica) 
    usando o Selenium WebDriver. Este cliente automatiza tarefas como login, seleção de instalação, 
    abertura de faturas e download de contas no site da EDP.

    Atributos:
        driver (WebDriver): A instância do Selenium WebDriver usada para automatizar ações no navegador.
        captcha (CaptchaClient): Uma instância de CaptchaClient usada para resolver captchas durante o login.

    Métodos:
        __init__(self, url: str, headless: bool = False, remote_url: str = None):
            Inicializa o EDPClient com a URL fornecida, opcionalmente executando no modo headless ou utilizando um WebDriver remoto.
        
        __go_to_url(self, url: str) -> None:
            Navega para a URL especificada usando o WebDriver.
        
        login(self, username: str, password: str) -> None:
            Realiza o login no site da EDP utilizando o nome de usuário e senha fornecidos. 
            Inclui a resolução do captcha, se presente.
        
        select_instalation(self, instalation: str = "0151129920") -> None:
            Seleciona a instalação especificada no site da EDP.

        open_bills(self, instalation: str) -> None:
            Verifica a instalação selecionada e navega para a seção de faturas.
        
        download_bills(self, dates: list) -> list:
            Faz o download das faturas para as datas especificadas. As datas devem ser fornecidas no formato "MM/AAAA".
        
        close(self) -> None:
            Fecha o navegador e encerra a sessão do WebDriver.
        
        take_screenshot(self) -> None:
            Captura uma captura de tela do estado atual do navegador, salvando-a em um local predefinido.
    """

    def __init__(
        self, url: str, headless: bool = False, remote_url: str = None
    ) -> None:
        log.info("Iniciando cliente EDP")
        log.info(f"Remote URL = {remote_url}")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": config.DONWLOAD_FOLDER,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "plugins.always_open_pdf_externally": True,
            },
        )
        # chrome_options.binary_location = "/usr/bin/google-chrome"
        chrome_options.add_argument("--window-size=1280,1024")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
        )
        if headless:
            log.info("Executando headless")
            chrome_options.add_argument("--headless")
        self.captcha = captcha_client.CaptchaClient()
        if remote_url:
            log.info("Executando em modo remoto")
            self.driver = webdriver.Remote(
                command_executor=remote_url, options=chrome_options
            )
        else:
            self.driver = webdriver.Chrome(options=chrome_options)
        log.info("Navegando para URL da EDP")
        self.__go_to_url(url)

    def __go_to_url(self, url: str) -> None:
        log.info(f"Acessando {url}")
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
            log.info("Quebrando Captcha")
            self.driver.execute_script(
                script=f"document.querySelector('textarea#g-recaptcha-response-100000').innerText = '{captcha_response}'"
            )
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, selectors.LOGIN["LOGIN_BTN"]))
        ).click()
        log.info("Validando se logou com sucesso")
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, selectors.INSTALACOES["HEADER"]))
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

    def close(self):
        log.info("Fechando navegador")
        self.driver.close()
        self.driver.quit()

    def take_screenshot(self):
        path = os.path.join(config.LOGS, "exception.png")
        self.driver.save_screenshot(path)
