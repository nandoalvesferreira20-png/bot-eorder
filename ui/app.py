import customtkinter as ctk

from ui.home import HomePage
from ui.relatorios import RelatoriosPage
from ui.sobre import SobrePage
from ui.splash import SplashScreen
from ui.theme import CORES
from version import APP_NAME, VERSION
from PIL import Image
from utils.resources import resource_path

logo = ctk.CTkImage(
    light_image=Image.open(resource_path("assets/bot_eorder.png")),
    dark_image=Image.open(resource_path("assets/bot_eorder.png")),
    size=(58, 58)
)
class BotEorderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Esconde a janela principal enquanto a splash aparece
        self.withdraw()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title(f"{APP_NAME} v{VERSION}")
        try:
            self.iconbitmap("assets/bot_eorder.ico")
        except Exception:
            pass
        self.geometry("1240x760")
        self.minsize(1100, 680)

        self.configure(
            fg_color=CORES["fundo"]
        )

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.criar_sidebar()
        self.criar_area_principal()
        self.exibir_pagina("status")

        # Abre a splash após carregar a interface
        self.splash = SplashScreen(
            self,
            duracao_ms=1800
        )

    def criar_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self,
            width=240,
            corner_radius=0,
            fg_color=CORES["sidebar"]
        )
        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )
        self.sidebar.grid_propagate(False)

        logo_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )
        logo_frame.pack(
            fill="x",
            padx=22,
            pady=(28, 30)
        )

        icone = ctk.CTkLabel(
            logo_frame,
            image=logo,
            text=""
            )
        icone.pack(side="left")
        texto_logo = ctk.CTkFrame(
            logo_frame,
            fg_color="transparent"
        )
        texto_logo.pack(
            side="left",
            padx=(12, 0)
        )

    

        titulo = ctk.CTkLabel(
            texto_logo,
            text="Bot eOrder",
            text_color=CORES["texto"],
            font=ctk.CTkFont(
                size=21,
                weight="bold"
            )
        )
        titulo.pack(anchor="w")

        subtitulo = ctk.CTkLabel(
            texto_logo,
            text="Automação de TdCs",
            text_color=CORES["texto_secundario"],
            font=ctk.CTkFont(size=12)
        )
        subtitulo.pack(anchor="w")

        label_menu = ctk.CTkLabel(
            self.sidebar,
            text="MENU PRINCIPAL",
            text_color=CORES["texto_secundario"],
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        )
        label_menu.pack(
            anchor="w",
            padx=24,
            pady=(0, 8)
        )

        self.botao_status = self.criar_botao_menu(
            texto="⌂  Dashboard",
            comando=lambda: self.exibir_pagina(
                "status"
            )
        )

        self.botao_relatorios = self.criar_botao_menu(
            texto="▤  Relatórios",
            comando=lambda: self.exibir_pagina(
                "relatorios"
            )
        )

        self.botao_sobre = self.criar_botao_menu(
            texto="ⓘ  Sobre",
            comando=lambda: self.exibir_pagina(
                "sobre"
            )
        )

        rodape = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )
        rodape.pack(
            side="bottom",
            fill="x",
            padx=22,
            pady=22
        )

        status = ctk.CTkLabel(
            rodape,
            text="● Sistema online",
            text_color=CORES["verde"],
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        )
        status.pack(anchor="w")

        versao = ctk.CTkLabel(
            rodape,
            text=f"Versão {VERSION}",
            text_color=CORES["texto_secundario"],
            font=ctk.CTkFont(size=11)
        )
        versao.pack(
            anchor="w",
            pady=(4, 0)
        )

    def criar_botao_menu(
        self,
        texto,
        comando
    ):
        botao = ctk.CTkButton(
            self.sidebar,
            text=texto,
            height=46,
            anchor="w",
            corner_radius=10,
            fg_color="transparent",
            hover_color=CORES["card_hover"],
            text_color=CORES["texto"],
            border_width=0,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            command=comando
        )
        botao.pack(
            fill="x",
            padx=16,
            pady=5
        )

        return botao

    def criar_area_principal(self):
        self.container = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=CORES["fundo"]
        )
        self.container.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.container.grid_columnconfigure(
            0,
            weight=1
        )
        self.container.grid_rowconfigure(
            0,
            weight=1
        )

        self.paginas = {
            "status": HomePage(self.container),
            "relatorios": RelatoriosPage(
                self.container
            ),
            "sobre": SobrePage(
                self.container
            )
        }

        for pagina in self.paginas.values():
            pagina.grid(
                row=0,
                column=0,
                sticky="nsew"
            )

    def exibir_pagina(self, nome):
        pagina = self.paginas[nome]
        pagina.tkraise()

        if nome == "relatorios":
            pagina.atualizar_lista()

        self.atualizar_menu_ativo(nome)

    def atualizar_menu_ativo(self, nome):
        botoes = {
            "status": self.botao_status,
            "relatorios": self.botao_relatorios,
            "sobre": self.botao_sobre
        }

        for nome_botao, botao in botoes.items():
            if nome_botao == nome:
                botao.configure(
                    fg_color=CORES["roxo"],
                    hover_color=CORES["roxo_hover"]
                )
            else:
                botao.configure(
                    fg_color="transparent",
                    hover_color=CORES["card_hover"]
                )


if __name__ == "__main__":
    app = BotEorderApp()
    app.mainloop()