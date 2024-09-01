from libs import edp_client as edp
from common import config, utils
from common.config import log
import argparse


def main_wokrflow(numero_instalacao: str, mes: list[str]):
    log.info("Iniciando fluxo de extração de fatura da EDP")
    edp_client = edp.EDPClient(url=config.URL, headless=False)  # type: ignore
    edp_client.login(username=config.EMAIL, password=config.PASSWORD)  # type: ignore
    edp_client.select_instalation()
    edp_client.open_bills(instalation=numero_instalacao)
    edp_client.download_bills(dates=mes)


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
    args = argparser.parse_args()
    # numero_instalacao
    # Mes
    utils.create_folder(config.DONWLOAD_FOLDER)
    utils.create_folder(config.LOGS)
    main_wokrflow(numero_instalacao=args.numero_instalacao, mes=args.mes)
    # --numero_instalacao 0151129920 --mes 03/2024
