from playwright.sync_api import sync_playwright


def abrir_eorder(url: str):
    playwright = sync_playwright().start()

    context = playwright.chromium.launch_persistent_context(
        user_data_dir="perfil_eorder",
        headless=False,
        slow_mo=300,
        viewport={"width": 1366, "height": 768},
        args=["--start-maximized"]
    )

    page = context.new_page()
    page.goto(url, wait_until="domcontentloaded", timeout=60000)

    return playwright, None, context, page