import customtkinter as ctk

from ui.home import HomePage


class BotEorderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Bot eOrder")
        self.geometry("1180x720")
        self.minsize(1050, 650)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.criar_sidebar()
        self.criar_area_principal()

    def criar_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0
        )
        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )
        self.sidebar.grid_propagate(False)

        titulo = ctk.CTkLabel(
            self.sidebar,
            text="BOT EORDER",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        )
        titulo.pack(
            pady=(35, 8)
        )

        subtitulo = ctk.CTkLabel(
            self.sidebar,
            text="Automação de TdCs",
            text_color="gray70",
            font=ctk.CTkFont(size=13)
        )
        subtitulo.pack(
            pady=(0, 30)
        )

        self.botao_status = ctk.CTkButton(
            self.sidebar,
            text="Status",
            height=42,
            anchor="w",
            command=self.exibir_home
        )
        self.botao_status.pack(
            fill="x",
            padx=20,
            pady=6
        )

        self.botao_relatorios = ctk.CTkButton(
            self.sidebar,
            text="Relatórios",
            height=42,
            anchor="w",
            fg_color="transparent",
            border_width=1
        )
        self.botao_relatorios.pack(
            fill="x",
            padx=20,
            pady=6
        )

        self.botao_sobre = ctk.CTkButton(
            self.sidebar,
            text="Sobre",
            height=42,
            anchor="w",
            fg_color="transparent",
            border_width=1
        )
        self.botao_sobre.pack(
            fill="x",
            padx=20,
            pady=6
        )

        versao = ctk.CTkLabel(
            self.sidebar,
            text="v1.0.0",
            text_color="gray60"
        )
        versao.pack(
            side="bottom",
            pady=20
        )

    def criar_area_principal(self):
        self.container = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="transparent"
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

        self.home_page = HomePage(
            self.container
        )
        self.home_page.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

    def exibir_home(self):
        self.home_page.tkraise()


if __name__ == "__main__":
    app = BotEorderApp()
    app.mainloop()