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

        self.grid_columnconfigure(1, weight=1)

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
            width=42,
            height=42,
            corner_radius=12,
            fg_color=cor_destaque,
            text_color=CORES["texto"],
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )
        label_icone.grid(
            row=0,
            column=1,
            rowspan=2,
            padx=(0, 12),
            pady=18
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
            pady=(18, 2)
        )

        self.label_valor = ctk.CTkLabel(
            self,
            text=valor_inicial,
            text_color=CORES["texto"],
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )
        self.label_valor.grid(
            row=1,
            column=2,
            sticky="nw",
            pady=(0, 18)
        )

    def atualizar_valor(self, valor):
        self.label_valor.configure(
            text=str(valor)
        )