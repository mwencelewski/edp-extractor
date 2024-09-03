from libs import edp_client as edp
from common import config, utils
from common.config import log
import argparse

"""
Este script automatiza o processo de extração de faturas da EDP utilizando o Selenium WebDriver. 
Ele permite que o usuário especifique o número da instalação e os meses para os quais as faturas 
devem ser baixadas. O script também suporta execução em modo headless e a captura de telas 
em caso de falha na navegação.

Funções:
    main_workflow(numero_instalacao: str, mes: list[str], headless: bool = True) -> None:
        Executa o fluxo principal de extração de faturas. Inicializa o cliente EDP, faz login, 
        seleciona a instalação, navega até a seção de faturas e realiza o download das faturas para 
        os meses especificados. Em caso de erro, captura uma captura de tela.

Uso:
    O script pode ser executado a partir da linha de comando com os seguintes argumentos:
        --numero_instalacao: O número da instalação para a qual as faturas serão extraídas (obrigatório).
        --mes: Um ou mais meses no formato MM/AAAA para buscar as faturas (obrigatório).
        --debug: Se especificado, o script será executado com o navegador visível (modo não headless).

Exemplo de uso:
    python script.py --numero_instalacao 12345678 --mes 03/2024 --mes 04/2024

"""


def main_workflow(
    numero_instalacao: str, mes: list[str], headless: bool = True
) -> None:
    log.info("Iniciando fluxo de extração de fatura da EDP")
    try:
        log.info(f"Endereço remoto do Selenium {config.SEL_SERVICE}")
        edp_client = edp.EDPClient(
            url=config.URL,  # type: ignore
            headless=headless,
            remote_url=config.SEL_SERVICE,  # type: ignore
        )  # type: ignore
        edp_client.login(username=config.EMAIL, password=config.PASSWORD)  # type: ignore
        edp_client.select_instalation()
        edp_client.open_bills(instalation=numero_instalacao)
        edp_client.download_bills(dates=mes)
        edp_client.close()
    except edp.TimeoutException:
        log.error("Falhou na navegação do site da EDP")
        edp_client.take_screenshot()  # type: ignore
        edp_client.close()  # type: ignore


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()

    argparser.add_argument(
        "--numero_instalacao",
        type=str,
        help="Número da instalação para buscar faturas",
        required=True,
    )
    argparser.add_argument(
        "--mes",
        type=str,
        action="append",
        required=True,
        help="Mês para buscar faturas. Ex: 03/2024",
    )
    argparser.add_argument("--debug", action="store_true")
    args = argparser.parse_args()
    headless = not args.debug
    utils.create_folder(config.DONWLOAD_FOLDER)
    utils.create_folder(config.LOGS)
    main_workflow(
        numero_instalacao=args.numero_instalacao, mes=args.mes, headless=headless
    )
    # --numero_instalacao 0151129920 --mes 03/2024 --mes 04/2024 --debug
