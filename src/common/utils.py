import os
from common.config import log

months_ptbr = {
    1: "JAN",
    2: "FEV",
    3: "MAR",
    4: "ABR",
    5: "MAI",
    6: "JUN",
    7: "JUL",
    8: "AGO",
    9: "SET",
    10: "OUT",
    11: "NOV",
    12: "DEZ",
}


def create_folder(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)
        log.info(f"Diretório criado: {path}")
    else:
        log.info(f"Diretório já existe: {path}")
