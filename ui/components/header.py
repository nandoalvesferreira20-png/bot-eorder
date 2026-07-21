import customtkinter as ctk

from ui.components.status_badge import StatusBadge
from ui.theme import CORES


class PageHeader(ctk.CTkFrame):
    def __init__(
        self,
        master,
        titulo: str,
        subtitulo: str
    ):
        super().__init__(
            master,
            fg_color="transparent"
        )

        self.grid_columnconfigure(0, weight=1)

        bloco_texto = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        bloco_texto.grid(
            row=0,
            column=0,
            sticky="w"
        )

        label_titulo = ctk.CTkLabel(
            bloco_texto,
            text=titulo,
            text_color=CORES["texto"],
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )
        label_titulo.pack(anchor="w")

        label_subtitulo = ctk.CTkLabel(
            bloco_texto,
            text=subtitulo,
            text_color=CORES["texto_secundario"],
            font=ctk.CTkFont(size=14)
        )
        label_subtitulo.pack(
            anchor="w",
            pady=(4, 0)
        )

        self.status_badge = StatusBadge(
            self,
            texto="Sistema online",
            cor=CORES["verde"]
        )
        self.status_badge.grid(
            row=0,
            column=1,
            sticky="e"
        )