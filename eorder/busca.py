import re


def abrir_busca_tdcs(frame):
    frame.locator("div").filter(
        has_text=re.compile(r"^Lista TdC$")
    ).first.click()

    frame.locator("div").filter(
        has_text=re.compile(r"^Busca TdCs$")
    ).first.click()


def pesquisar_tdc(frame, centro_operativo: str, codigo_externo: str):
    garantir_filtros_abertos(frame)

    campo_centro = frame.locator('select[name="_lyAODLID_AFIL"]')
    campo_codigo = frame.locator('input[name="_syXWFMAODLCODICEESTERNO"]')

    campo_centro.wait_for(state="visible", timeout=30000)
    campo_centro.select_option(centro_operativo, force=True)

    campo_codigo.wait_for(state="visible", timeout=30000)
    campo_codigo.click(force=True)
    campo_codigo.press("Control+A")
    campo_codigo.press("Backspace")
    campo_codigo.type(codigo_externo, delay=50)

    botao_buscar = frame.locator('button.butSub.butAct:has-text("Busca")')
    botao_buscar.wait_for(state="visible", timeout=30000)
    botao_buscar.click(force=True)

    frame.locator("div.badged img.icon_menu[alt='Opções']").last.wait_for(timeout=30000)

    print("Pesquisa realizada.")

def garantir_filtros_abertos(frame):
    campo_centro = frame.locator('select[name="_lyAODLID_AFIL"]')

    try:
        if campo_centro.is_visible(timeout=3000):
            return
    except:
        pass

    botao_filtros = frame.get_by_role("button", name="filtros").first

    botao_filtros.wait_for(timeout=30000)
    botao_filtros.click(force=True)

    campo_centro.wait_for(timeout=30000)

    print("Filtros abertos.")