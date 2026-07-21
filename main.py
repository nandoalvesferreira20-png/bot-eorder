from config.config import EORDER_URL, EXCEL_PATH
from core.executor import BotEorderExecutor
from ui.app import BotEorderApp


def aguardar_login():
    input(
        "Faça login no eOrder e aperte ENTER "
        "aqui no terminal para continuar..."
    )


def exibir_log(mensagem: str):
    print(mensagem)


def exibir_progresso(
    processadas,
    total,
    estatisticas
):
    print(
        f"Progresso: {processadas}/{total} | "
        f"Canceladas: {estatisticas.canceladas} | "
        f"Anuladas: {estatisticas.ja_anuladas} | "
        f"Finalizadas: {estatisticas.wo_finalizadas} | "
        f"Erros: {estatisticas.erros}"
    )


def main():
    executor = BotEorderExecutor(
        eorder_url=EORDER_URL,
        excel_path=EXCEL_PATH,
        callback_log=exibir_log,
        callback_progresso=exibir_progresso,
        callback_login=aguardar_login
    )

    estatisticas = executor.executar()

    if estatisticas:
        estatisticas.exibir_resumo(
            tempo_total="Consulte o relatório"
        )

    input(
        "\nPressione ENTER para encerrar..."
    )


if __name__ == "__main__":
    app = BotEorderApp()
    app.mainloop()