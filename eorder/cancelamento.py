from eorder.busca import pesquisar_tdc

def abrir_menu_opcoes(frame):
    menu_opcoes = frame.get_by_role("img", name="Opções")
    menu_opcoes.wait_for(timeout=30000)
    menu_opcoes.click()
    print("Menu de opções aberto.")


def clicar_cancelar_selecionados(frame):
    cancelar = frame.get_by_text("Cancelar selecionados", exact=True).last

    cancelar.wait_for(timeout=30000)
    cancelar.click(force=True)

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

def processar_tdc(frame, centro_operativo: str, codigo_externo: str):
    print(f"Processando TdC: {codigo_externo}")

    pesquisar_tdc(
        frame,
        centro_operativo=centro_operativo,
        codigo_externo=codigo_externo
    )

    abrir_menu_opcoes(frame)
    clicar_cancelar_selecionados(frame)
    confirmar_popup_sim(frame)
    confirmar_cancelamento(frame)
    fechar_popup_resultado(frame)
    fechar_tela_cancelamento(frame)

    print(f"TdC processada: {codigo_externo}")