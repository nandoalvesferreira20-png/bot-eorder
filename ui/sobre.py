import customtkinter as ctk
from PIL import Image

from ui.components.header import PageHeader
from ui.theme import CORES
from version import APP_NAME, VERSION, DESCRIPTION, AUTHOR
from utils.resources import resource_path


class SobrePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color=CORES["fundo"]
        )

        self.logo = ctk.CTkImage(
            light_image=Image.open(
                resource_path("assets/bot_eorder.png")
            ),
            dark_image=Image.open(
                resource_path("assets/bot_eorder.png")
            ),
            size=(110, 110)
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.criar_header()
        self.criar_conteudo()

    def criar_header(self):
        self.header = PageHeader(
            self,
            titulo="ⓘ Sobre",
            subtitulo=f"Informações sobre o {APP_NAME}."
        )

        self.header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=30,
            pady=(25, 15)
        )

    def criar_conteudo(self):
        card = ctk.CTkFrame(
            self,
            corner_radius=16,
            fg_color=CORES["card"],
            border_width=1,
            border_color=CORES["borda"]
        )
        card.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=30,
            pady=(0, 25)
        )

        bloco_icone = ctk.CTkLabel(
            card,
            image=self.logo,
            text=""
        )
        bloco_icone.pack(
            pady=(40, 20)
        )

        titulo = ctk.CTkLabel(
            card,
            text=APP_NAME,
            text_color=CORES["texto"],
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )
        titulo.pack(
            pady=(0, 8)
        )

        versao = ctk.CTkLabel(
            card,
            text=f"Versão {VERSION}",
            text_color=CORES["texto_secundario"],
            font=ctk.CTkFont(size=14)
        )
        versao.pack(
            pady=(0, 20)
        )

        subtitulo = ctk.CTkLabel(
            card,
            text=DESCRIPTION,
            text_color=CORES["roxo"],
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )
        subtitulo.pack(
            pady=(0, 20)
        )

        descricao = ctk.CTkLabel(
            card,
            text=(
                "Automação desenvolvida para processar "
                "cancelamentos de TdCs em lote.\n\n"
                "A aplicação realiza leitura de planilhas, "
                "navegação automatizada, tratamento de exceções, "
                "registro de logs, screenshots de erro e "
                "geração de relatórios em Excel."
            ),
            text_color=CORES["texto"],
            justify="center",
            wraplength=650,
            font=ctk.CTkFont(size=15)
        )
        descricao.pack(
            padx=40,
            pady=(0, 30)
        )

        tecnologias = ctk.CTkLabel(
            card,
            text=(
                "Tecnologias utilizadas\n\n"
                "Python • Playwright • OpenPyXL • "
                "CustomTkinter • Git"
            ),
            text_color=CORES["roxo"],
            justify="center",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )
        tecnologias.pack(
            pady=(0, 30)
        )

        autoria = ctk.CTkLabel(
            card,
            text=f"Desenvolvido por {AUTHOR}",
            text_color=CORES["texto_secundario"],
            font=ctk.CTkFont(size=13)
        )
        autoria.pack(
            side="bottom",
            pady=25
        )