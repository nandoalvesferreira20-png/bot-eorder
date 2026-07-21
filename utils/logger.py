import logging
from datetime import datetime
from pathlib import Path


def configurar_logger():
    pasta_logs = Path("logs")
    pasta_logs.mkdir(parents=True, exist_ok=True)

    identificador_execucao = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho_log = pasta_logs / f"execucao_{identificador_execucao}.log"

    logger = logging.getLogger("bot_eorder")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Evita duplicação de mensagens em novas execuções
    logger.handlers.clear()

    formato = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler_arquivo = logging.FileHandler(
        caminho_log,
        encoding="utf-8"
    )
    handler_arquivo.setFormatter(formato)

    handler_console = logging.StreamHandler()
    handler_console.setFormatter(formato)

    logger.addHandler(handler_arquivo)
    logger.addHandler(handler_console)

    return logger, caminho_log, identificador_execucao