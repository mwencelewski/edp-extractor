from twocaptcha import TwoCaptcha
from common import config
from common.config import log
from dataclasses import dataclass

solver = TwoCaptcha("1329ea27f1877943d09606bbdddca6b8")


@dataclass
class CaptchaException(Exception):
    instalacao: str

    def __str__(self) -> str:
        return f"Failed login attempt to instalacao: {self.instalacao}"


class CaptchaClient:
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
