from twocaptcha import TwoCaptcha
from common import config
from common.config import log
from dataclasses import dataclass

solver = TwoCaptcha(config.APIKEY)


@dataclass
class CaptchaException(Exception):
    instalacao: str

    def __str__(self) -> str:
        return f"Failed login attempt to instalacao: {self.instalacao}"


class CaptchaClient:
    """
    CaptchaClient é uma classe utilizada para resolver captchas utilizando o serviço TwoCaptcha,
    que é especialmente útil em processos de automação web onde captchas precisam ser resolvidos
    para prosseguir com a execução.

    Classes:
        CaptchaException(Exception):
            Exceção personalizada que é lançada quando ocorre uma falha ao tentar resolver o captcha.

        CaptchaClient:
            Cliente para resolver captchas utilizando a API do TwoCaptcha.

    Métodos:
        CaptchaException(instalacao: str):
            Constrói uma exceção personalizada com base na instalação onde a falha ocorreu.

        __str__(self) -> str:
            Retorna uma string descritiva da exceção, indicando a instalação onde a tentativa de login falhou.

        solve_captcha(self) -> str:
            Resolve um captcha utilizando o serviço TwoCaptcha. Retorna o código do captcha resolvido ou
            lança uma exceção CaptchaException se a resolução falhar.

        captcha_solver(self) -> str:
            Tenta resolver o captcha até 4 vezes, logando cada tentativa. Se conseguir resolver,
            retorna o código do captcha. Caso contrário, a exceção CaptchaException é lançada.
    """

    def solve_captcha(self):
        result = solver.recaptcha(
            sitekey=config.SITEKEY,
            url="https://www.edponline.com.br/para-sua-casa/login",
            version="v3",
        )

        if "captchaId" in result:
            log.info(f"CAPTCHA ID: {result['captchaId']}")
        if "code" in result:
            log.info(f"CAPTCHA CODE: {result['code']}")
            return result["code"]
        else:
            log.error(f"Failed to solve captcha: {result}")
            raise CaptchaException("Failed to Solve Captcha")

    def captcha_solver(self):
        for i in range(1, 5):
            log.info(f"Attempt {i} to solve captcha")
            try:
                return self.solve_captcha()
            except CaptchaException as e:
                log.error(e)
                continue
