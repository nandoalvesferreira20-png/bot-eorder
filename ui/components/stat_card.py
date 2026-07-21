import customtkinter as ctk

from ui.theme import CORES


class StatCard(ctk.CTkFrame):
    def __init__(
        self,
        master,
        titulo: str,
        icone: str,
        cor_destaque: str,
        valor_inicial: str = "0"
    ):
        super().__init__(
            master,
            corner_radius=16,
            fg_color=CORES["card"],
            border_width=1,
            border_color=CORES["borda"]
        )

        self.grid_columnconfigure(2, weight=1)

        faixa = ctk.CTkFrame(
            self,
            width=6,
            corner_radius=8,
            fg_color=cor_destaque
        )
        faixa.grid(
            row=0,
            column=0,
            rowspan=2,
            sticky="ns",
            padx=(0, 14),
            pady=12
        )

        label_icone = ctk.CTkLabel(
            self,
            text=icone,
            width=52,
            height=52,
            corner_radius=14,
            fg_color=cor_destaque,
            text_color=CORES["texto"],
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )
        label_icone.grid(
            row=0,
            column=1,
            rowspan=2,
            padx=(0, 14),
            pady=24
        )

        self.label_titulo = ctk.CTkLabel(
            self,
            text=titulo,
            text_color=CORES["texto_secundario"],
            font=ctk.CTkFont(size=13)
        )
        self.label_titulo.grid(
            row=0,
            column=2,
            sticky="sw",
            pady=(24, 2)
        )

        self.label_valor = ctk.CTkLabel(
            self,
            text=valor_inicial,
            text_color=CORES["texto"],
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )
        self.label_valor.grid(
            row=1,
            column=2,
            sticky="nw",
            pady=(0, 24)
        )

    def atualizar_valor(self, valor):
        self.label_valor.configure(
            text=str(valor)
        )