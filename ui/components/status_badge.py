import customtkinter as ctk

from ui.theme import CORES


class StatusBadge(ctk.CTkFrame):
    def __init__(
        self,
        master,
        texto="Pronto",
        cor=None
    ):
        cor = cor or CORES["verde"]

        super().__init__(
            master,
            fg_color=CORES["card"],
            corner_radius=12,
            border_width=1,
            border_color=CORES["borda"]
        )

        self.indicador = ctk.CTkLabel(
            self,
            text="●",
            text_color=cor,
            font=ctk.CTkFont(size=14)
        )
        self.indicador.pack(
            side="left",
            padx=(12, 6),
            pady=8
        )

        self.label = ctk.CTkLabel(
            self,
            text=texto,
            text_color=CORES["texto"],
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        )
        self.label.pack(
            side="left",
            padx=(0, 12),
            pady=8
        )

    def atualizar(self, texto, cor):
        self.indicador.configure(
            text_color=cor
        )
        self.label.configure(
            text=texto
        )