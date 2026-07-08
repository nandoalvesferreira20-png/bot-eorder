import re


def abrir_busca_tdcs(frame):
    frame.locator("div").filter(
        has_text=re.compile(r"^Lista TdC$")
    ).first.click()

    frame.locator("div").filter(
        has_text=re.compile(r"^Busca TdCs$")
    ).first.click()


def pesquisar_tdc(frame, centro_operativo: str, codigo_externo: str):
    campo_centro = frame.locator('select[name="_lyAODLID_AFIL"]')
    campo_codigo = frame.locator('input[name="_syXWFMAODLCODICEESTERNO"]')

    campo_centro.wait_for(timeout=30000)
    campo_centro.select_option(centro_operativo)

    campo_codigo.wait_for(timeout=30000)
    campo_codigo.click()
    campo_codigo.fill(codigo_externo)

    botao_buscar = frame.locator('button.butSub.butAct:has-text("Busca")')
    botao_buscar.wait_for(timeout=30000)
    botao_buscar.click()

    print("Pesquisa realizada.")