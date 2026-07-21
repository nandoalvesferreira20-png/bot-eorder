from pathlib import Path

from playwright.sync_api import sync_playwright


def abrir_eorder(url: str):
    playwright = sync_playwright().start()

    pasta_perfil = (
        Path.home()
        / "AppData"
        / "Local"
        / "BotEorder"
        / "perfil_eorder"
    )

    pasta_perfil.mkdir(
        parents=True,
        exist_ok=True
    )

    context = playwright.chromium.launch_persistent_context(
        user_data_dir=str(pasta_perfil),
        channel="chrome",
        headless=False,
        slow_mo=300,
        no_viewport=True,
        args=["--start-maximized"]
    )

    paginas = context.pages

    if paginas:
        page = paginas[0]
    else:
        page = context.new_page()

    page.goto(
        url,
        wait_until="domcontentloaded",
        timeout=60000
    )

    return playwright, None, context, page