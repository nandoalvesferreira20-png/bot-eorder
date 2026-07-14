import re
import unicodedata
import time
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

def abrir_busca_tdcs(frame):
    busca_tdcs = frame.locator("div").filter(
        has_text=re.compile(r"^Busca TdCs$")
    ).first

    # Se o submenu já estiver aberto, só clica em Busca TdCs
    try:
        if busca_tdcs.is_visible(timeout=3000):
            busca_tdcs.click(force=True)
            print("Tela Busca TdCs aberta.")
            return
    except:
        pass

    # Se não estiver aberto, expande Lista TdC
    lista_tdc = frame.locator("div").filter(
        has_text=re.compile(r"^Lista TdC$")
    ).first

    lista_tdc.wait_for(timeout=30000)
    lista_tdc.click(force=True)

    busca_tdcs.wait_for(timeout=30000)
    busca_tdcs.click(force=True)

    print("Tela Busca TdCs aberta.")


def pesquisar_tdc(frame, centro_operativo: str, codigo_externo: str):
    garantir_filtros_abertos(frame)

    campo_centro = frame.locator('select[name="_lyAODLID_AFIL"]')
    campo_codigo = frame.locator('input[name="_syXWFMAODLCODICEESTERNO"]')

    campo_centro.wait_for(state="visible", timeout=30000)
    selecionar_centro_operativo(
        campo_centro,
        centro_operativo
    )

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

def garantir_filtros_abertos(frame, tentativas: int = 3):
    campo_centro = frame.locator(
        'select[name="_lyAODLID_AFIL"]'
    )

    for tentativa in range(1, tentativas + 1):
        print(
            f"Tentando preparar os filtros "
            f"({tentativa}/{tentativas})..."
        )

        # Caso os campos já estejam abertos
        try:
            if campo_centro.is_visible(timeout=3000):
                print("Filtros já estão abertos.")
                return
        except Exception:
            pass

        # Procura todos os botões chamados "filtros"
        botoes_filtros = frame.get_by_role(
            "button",
            name="filtros"
        )

        quantidade = botoes_filtros.count()

        for indice in range(quantidade):
            botao = botoes_filtros.nth(indice)

            try:
                if botao.is_visible(timeout=1000):
                    botao.click(force=True)

                    campo_centro.wait_for(
                        state="visible",
                        timeout=15000
                    )

                    print("Filtros abertos.")
                    return

            except PlaywrightTimeoutError:
                continue
            except Exception:
                continue

        print(
            "Botão filtros não disponível. "
            "Tentando recuperar a tela Busca TdCs..."
        )

        try:
            abrir_busca_tdcs(frame)
        except Exception as erro:
            print(f"Falha ao reabrir Busca TdCs: {erro}")

        time.sleep(2)

    raise RuntimeError(
        "Não foi possível abrir os filtros "
        f"após {tentativas} tentativas."
    )


def normalizar_texto(texto: str) -> str:
    texto = str(texto or "").strip().upper()

    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )

    return " ".join(texto.split())


def selecionar_centro_operativo(campo_centro, centro_operativo: str):
    centro_procurado = normalizar_texto(centro_operativo)

    campo_centro.wait_for(
        state="visible",
        timeout=30000
    )

    opcoes = campo_centro.locator("option")
    quantidade = opcoes.count()

    for indice in range(quantidade):
        opcao = opcoes.nth(indice)

        texto_opcao = normalizar_texto(
            opcao.text_content()
        )

        valor_opcao = normalizar_texto(
            opcao.get_attribute("value")
        )

        if (
            centro_procurado == texto_opcao
            or centro_procurado == valor_opcao
            or centro_procurado in texto_opcao
        ):
            valor_real = opcao.get_attribute("value")

            campo_centro.select_option(
                value=valor_real
            )

            print(
                f"Centro Operativo selecionado: "
                f"{opcao.text_content().strip()}"
            )

            return

    raise ValueError(
        f"Centro Operativo não encontrado no eOrder: "
        f"{centro_operativo}"
    )