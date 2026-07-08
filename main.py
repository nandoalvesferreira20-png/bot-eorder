from config.config import EORDER_URL, EXCEL_PATH
from excel.leitor_excel import ler_notas_excel
from browser.navegador import abrir_eorder
from eorder.busca import abrir_busca_tdcs
from eorder.cancelamento import processar_tdc


def main():
    notas = ler_notas_excel(EXCEL_PATH)

    print(f"Notas carregadas: {len(notas)}")

    if not notas:
        print("Nenhuma nota encontrada.")
        return

    playwright, browser, context, page = abrir_eorder(EORDER_URL)

    input("Faça login no eOrder e aperte ENTER aqui no terminal para continuar...")

    frame = page.frame_locator('iframe[name="mainFrame"]')

    frame.get_by_text("Menu Principal").wait_for(timeout=30000)

    abrir_busca_tdcs(frame)

    for indice, nota in enumerate(notas, start=1):
        centro_operativo = "481"  # temporário
        codigo_externo = nota["codigo_externo"]

        print(f"\n[{indice}/{len(notas)}] Iniciando {codigo_externo}")

        try:
            processar_tdc(
                frame,
                centro_operativo=centro_operativo,
                codigo_externo=codigo_externo
            )

            print(f"[{indice}/{len(notas)}] OK - {codigo_externo}")

        except Exception as erro:
            print(f"[{indice}/{len(notas)}] ERRO - {codigo_externo}")
            print(f"Motivo: {erro}")
            continue

    print("Sprint 4 finalizado: loop concluído.")

    input("Pressione ENTER para fechar o navegador...")

    context.close()

    if browser:
        browser.close()

    playwright.stop()


if __name__ == "__main__":
    main()