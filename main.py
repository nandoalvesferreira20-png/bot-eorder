from config.config import EORDER_URL, EXCEL_PATH
from excel.leitor_excel import ler_notas_excel
from browser.navegador import abrir_eorder
from eorder.busca import abrir_busca_tdcs, pesquisar_tdc
from eorder.cancelamento import (
    abrir_menu_opcoes,
    clicar_cancelar_selecionados,
    confirmar_popup_sim,
    confirmar_cancelamento,
    fechar_popup_resultado,
    fechar_tela_cancelamento,
)


def main():
    notas = ler_notas_excel(EXCEL_PATH)

    print(f"Notas carregadas: {len(notas)}")

    if not notas:
        print("Nenhuma nota encontrada.")
        return

    primeira_nota = notas[0]
    print("Primeira nota:", primeira_nota)

    playwright, browser, context, page = abrir_eorder(EORDER_URL)

    input("Faça login no eOrder e aperte ENTER aqui no terminal para continuar...")

    frame = page.frame_locator('iframe[name="mainFrame"]')

    frame.get_by_text("Menu Principal").wait_for(timeout=30000)

    abrir_busca_tdcs(frame)

    pesquisar_tdc(
        frame,
        centro_operativo="481",
        codigo_externo=primeira_nota["codigo_externo"]
    )

    input("Confira se a pesquisa encontrou a TdC. Aperte ENTER para abrir o menu...")

    abrir_menu_opcoes(frame)

    input("Menu aberto. Aperte ENTER para clicar em Cancelar selecionados...")

    clicar_cancelar_selecionados(frame)

    input("Popup 'Sim' aberto. Aperte ENTER para confirmar...")

    confirmar_popup_sim(frame)

    input("Tela de confirmação aberta. ENTER para confirmar cancelamento...")

    confirmar_cancelamento(frame)

    input("Popup de resultado aberto. ENTER para fechar...")

    fechar_popup_resultado(frame)

    input("Popup fechado. ENTER para fechar a tela de cancelamento...")

    fechar_tela_cancelamento(frame)

    print("Sprint 3 finalizado: cancelamento confirmado.")

    input("Pressione ENTER para fechar o navegador...")

    context.close()

    if browser:
        browser.close()

    playwright.stop()


if __name__ == "__main__":
    main()