from config.config import EORDER_URL, EXCEL_PATH
from excel.leitor_excel import ler_notas_excel
from browser.navegador import abrir_eorder
from eorder.busca import abrir_busca_tdcs
from eorder.cancelamento import processar_tdc


def reiniciar_fluxo(page):
    print("\nReiniciando o fluxo do eOrder...")

    page.reload(
        wait_until="domcontentloaded",
        timeout=60000
    )

    frame = page.frame_locator('iframe[name="mainFrame"]')

    frame.get_by_text("Menu Principal").wait_for(
        timeout=60000
    )

    abrir_busca_tdcs(frame)

    print("Fluxo reiniciado com sucesso.")

    return frame


def main():
    notas = ler_notas_excel(EXCEL_PATH)

    print(f"Notas carregadas: {len(notas)}")

    if not notas:
        print("Nenhuma nota encontrada.")
        return

    playwright, browser, context, page = abrir_eorder(EORDER_URL)

    try:
        input(
            "Faça login no eOrder e aperte ENTER "
            "aqui no terminal para continuar..."
        )

        frame = page.frame_locator('iframe[name="mainFrame"]')

        frame.get_by_text("Menu Principal").wait_for(
            timeout=30000
        )

        for indice, nota in enumerate(notas, start=1):
            centro_operativo = nota["centro_operativo"]
            codigo_externo = nota["codigo_externo"]

            print(
                f"\n[{indice}/{len(notas)}] "
                f"Iniciando {codigo_externo}"
            )

            tentativa = 1
            max_tentativas = 2

            while tentativa <= max_tentativas:
                try:
                    abrir_busca_tdcs(frame)

                    resultado = processar_tdc(
                        frame,
                        centro_operativo=centro_operativo,
                        codigo_externo=codigo_externo
                    )

                    if resultado == "JA_ANULADA":
                        print(
                            f"[{indice}/{len(notas)}] PULADA - "
                            f"{codigo_externo} já estava anulada"
                        )

                    elif resultado == "WO_FINALIZADA":
                        print(
                            f"[{indice}/{len(notas)}] PULADA - "
                            f"{codigo_externo} possui WO finalizada"
                        )

                    else:
                        print(
                            f"[{indice}/{len(notas)}] OK - "
                            f"{codigo_externo}"
                        )

                    break

                except Exception as erro:
                    mensagem_erro = str(erro)

                    print(
                        f"\nErro na tentativa "
                        f"{tentativa}/{max_tentativas}"
                    )
                    print(f"TdC: {codigo_externo}")
                    print(f"Motivo: {erro}")

                    erro_filtros = (
                        'name="filtros"' in mensagem_erro
                        or "Não foi possível abrir os filtros" in mensagem_erro
                    )

                    if erro_filtros and tentativa < max_tentativas:
                        print(
                            "Erro ao abrir filtros. "
                            "O bot reiniciará o fluxo e tentará "
                            "a mesma TdC novamente."
                        )

                        frame = reiniciar_fluxo(page)
                        tentativa += 1
                        continue

                    print(
                        "\nNão foi possível recuperar automaticamente."
                    )

                    input(
                        "Ajuste o eOrder manualmente para Busca TdCs "
                        "e aperte ENTER para seguir para a próxima nota..."
                    )

                    break

        print("\nProcessamento da planilha concluído.")

        input(
            "Pressione ENTER para fechar o navegador..."
        )

    finally:
        context.close()

        if browser:
            browser.close()

        playwright.stop()


if __name__ == "__main__":
    main()