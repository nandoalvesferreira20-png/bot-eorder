def abrir_menu_opcoes(frame):
    menu_opcoes = frame.get_by_role("img", name="Opções")
    menu_opcoes.wait_for(timeout=30000)
    menu_opcoes.click()
    print("Menu de opções aberto.")


def clicar_cancelar_selecionados(frame):
    cancelar = frame.locator("div").filter(
        has_text="Cancelar selecionados"
    ).nth(2)

    cancelar.wait_for(timeout=30000)
    cancelar.click()

    print("Cancelar selecionados clicado.")

def confirmar_popup_sim(frame):
    botao_sim = frame.locator("#btnOk")

    botao_sim.wait_for(timeout=30000)
    botao_sim.click()

    print("Popup 'Sim' confirmado.")

def confirmar_cancelamento(frame):
    botao_confirmar = frame.get_by_role(
        "button",
        name="confirmar Cancelamento"
    )

    botao_confirmar.wait_for(timeout=30000)
    botao_confirmar.click()

    print("Cancelamento confirmado.")

def fechar_popup_resultado(frame):
    botao_fechar = frame.locator("img.icon_x").first

    botao_fechar.wait_for(timeout=30000)
    botao_fechar.click(force=True)

    print("Popup de resultado fechado.")

def fechar_tela_cancelamento(frame):
    botao_fechar = frame.locator("div.tbi").filter(
        has_text="Fechar"
    ).first

    botao_fechar.wait_for(timeout=30000)
    botao_fechar.click(force=True)

    print("Tela de cancelamento fechada.")