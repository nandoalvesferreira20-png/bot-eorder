from eorder.busca import pesquisar_tdc
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
import re
import time


def abrir_menu_opcoes(frame):
    menu_opcoes = frame.locator(
        'div.badged img.icon_menu[alt="Opções"]'
    ).last

    menu_opcoes.wait_for(state="visible", timeout=30000)
    menu_opcoes.click(force=True)

    frame.get_by_text(
        "Cancelar selecionados",
        exact=True
    ).wait_for(timeout=30000)

    print("Menu de opções aberto.")


def clicar_cancelar_selecionados(frame):
    cancelar = frame.get_by_text(
        "Cancelar selecionados",
        exact=True
    ).last

    cancelar.wait_for(timeout=30000)
    cancelar.click(force=True)

    print("Cancelar selecionados clicado.")


def confirmar_popup_sim(frame):
    botao_sim = frame.locator("#btnOk")

    botao_sim.wait_for(timeout=30000)
    botao_sim.click()

    print("Popup 'Sim' confirmado.")


def obter_status_wo(frame) -> str:
    celulas_status = frame.locator("td.tvCell")

    status_conhecidos = [
        "Anulado",
        "Finalizado",
        "Programável",
    ]

    for status in status_conhecidos:
        elemento = celulas_status.filter(
            has_text=re.compile(rf"^{re.escape(status)}$")
        ).first

        try:
            if elemento.is_visible(timeout=1500):
                return status
        except Exception:
            continue

    return "DESCONHECIDO"


def confirmar_cancelamento(frame):
    botao_confirmar = frame.get_by_role(
        "button",
        name="confirmar Cancelamento"
    )

    botao_confirmar.wait_for(timeout=30000)
    botao_confirmar.click()

    print("Cancelamento confirmado.")


def tratar_resultado_cancelamento(frame):
    botao_fechar_popup = frame.locator("img.icon_x").first

    try:
        botao_fechar_popup.wait_for(
            state="visible",
            timeout=5000
        )

        botao_fechar_popup.click(force=True)

        print("Popup de resultado fechado.")

        return "POPUP_FECHADO"

    except PlaywrightTimeoutError:
        print(
            "Popup de resultado não apareceu. "
            "Verificando painel de resultado..."
        )

    os_cancelada = frame.get_by_text(
        "OS cancelada",
        exact=True
    )

    os_nao_cancelada = frame.get_by_text(
        "OS não cancelada",
        exact=True
    )

    os_pendente = frame.get_by_text(
        "OS pendente",
        exact=True
    )

    algum_resultado_visivel = (
        os_cancelada.is_visible(timeout=2000)
        or os_nao_cancelada.is_visible(timeout=2000)
        or os_pendente.is_visible(timeout=2000)
    )

    if algum_resultado_visivel:
        print(
            "Resultado exibido diretamente no painel. "
            "Continuando o fluxo."
        )

        return "PAINEL_RESULTADO"

    raise RuntimeError(
        "Não foi possível identificar o resultado "
        "do cancelamento."
    )


def fechar_tela_cancelamento(frame):
    botao_fechar = frame.locator("div.tbi").filter(
        has_text="Fechar"
    ).first

    botao_fechar.wait_for(timeout=30000)
    botao_fechar.click(force=True)

    print("Tela de cancelamento fechada.")


def processar_tdc(frame, centro_operativo: str, codigo_externo: str):
    print(f"Processando TdC: {codigo_externo}")

    pesquisar_tdc(
        frame,
        centro_operativo=centro_operativo,
        codigo_externo=codigo_externo
    )

    time.sleep(1.5)

    abrir_menu_opcoes(frame)
    clicar_cancelar_selecionados(frame)
    confirmar_popup_sim(frame)

    status_wo = obter_status_wo(frame)

    print(f"Status da WO: {status_wo}")

    if status_wo == "Anulado":
        print(f"TdC já estava anulada: {codigo_externo}")

        fechar_tela_cancelamento(frame)

        return "JA_ANULADA"

    if status_wo == "Finalizado":
        print(
            f"TdC não pode ser cancelada porque a WO "
            f"está finalizada: {codigo_externo}"
        )

        fechar_tela_cancelamento(frame)

        return "WO_FINALIZADA"

    confirmar_cancelamento(frame)
    tratar_resultado_cancelamento(frame)
    fechar_tela_cancelamento(frame)

    time.sleep(1.5)

    print(f"TdC processada: {codigo_externo}")

    return "CANCELADA"