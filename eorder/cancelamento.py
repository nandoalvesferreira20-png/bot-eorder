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