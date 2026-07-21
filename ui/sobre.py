import customtkinter as ctk


class SobrePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color="transparent"
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.criar_header()
        self.criar_conteudo()

    def criar_header(self):
        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=30,
            pady=(25, 15)
        )

        titulo = ctk.CTkLabel(
            header,
            text="Sobre",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )
        titulo.pack(anchor="w")

        subtitulo = ctk.CTkLabel(
            header,
            text="Informações sobre o Bot eOrder.",
            text_color="gray70",
            font=ctk.CTkFont(size=14)
        )
        subtitulo.pack(
            anchor="w",
            pady=(4, 0)
        )

    def criar_conteudo(self):
        card = ctk.CTkFrame(
            self,
            corner_radius=14
        )
        card.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=30,
            pady=(0, 25)
        )

        titulo = ctk.CTkLabel(
            card,
            text="BOT EORDER",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )
        titulo.pack(
            pady=(45, 8)
        )

        versao = ctk.CTkLabel(
            card,
            text="Versão 1.0.0",
            text_color="gray70",
            font=ctk.CTkFont(size=14)
        )
        versao.pack(
            pady=(0, 25)
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
                "Tecnologias\n\n"
                "Python • Playwright • OpenPyXL • "
                "CustomTkinter • Git"
            ),
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
            text="Desenvolvido por Fernando Alves",
            text_color="gray70",
            font=ctk.CTkFont(size=13)
        )
        autoria.pack(
            side="bottom",
            pady=25
        )