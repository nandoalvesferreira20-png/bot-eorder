import re
from datetime import datetime
from pathlib import Path


def limpar_nome_arquivo(texto: str) -> str:
    return re.sub(
        r'[<>:"/\\|?*]',
        "_",
        str(texto)
    )


def salvar_screenshot_erro(
    page,
    codigo_externo: str,
    identificador_execucao: str
):
    pasta = Path("screenshots") / identificador_execucao
    pasta.mkdir(parents=True, exist_ok=True)

    horario = datetime.now().strftime("%H%M%S")
    codigo_limpo = limpar_nome_arquivo(codigo_externo)

    caminho = pasta / (
        f"erro_{codigo_limpo}_{horario}.png"
    )

    page.screenshot(
        path=str(caminho),
        full_page=True
    )

    return caminho