import customtkinter as ctk
from PIL import Image

from ui.theme import CORES
from utils.resources import resource_path
from version import APP_NAME, VERSION, DESCRIPTION


class SplashScreen(ctk.CTkToplevel):
    def __init__(self, master, duracao_ms=1800):
        super().__init__(master)

        self.master = master
        self.duracao_ms = duracao_ms

        self.logo = ctk.CTkImage(
            light_image=Image.open(
                resource_path("assets/bot_eorder.png")
            ),
            dark_image=Image.open(
                resource_path("assets/bot_eorder.png")
            ),
            size=(90, 90)
        )

        self.overrideredirect(True)
        self.attributes("-topmost", True)

        largura = 460
        altura = 320

        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()

        pos_x = (largura_tela - largura) // 2
        pos_y = (altura_tela - altura) // 2

        self.geometry(
            f"{largura}x{altura}+{pos_x}+{pos_y}"
        )

        self.configure(
            fg_color=CORES["fundo"]
        )

        container = ctk.CTkFrame(
            self,
            corner_radius=22,
            fg_color=CORES["card"],
            border_width=1,
            border_color=CORES["borda"]
        )
        container.pack(
            fill="both",
            expand=True,
            padx=2,
            pady=2
        )

        icone = ctk.CTkLabel(
            container,
            image=self.logo,
            text=""
        )
        icone.pack(
            pady=(38, 16)
        )

        titulo = ctk.CTkLabel(
            container,
            text=APP_NAME,
            text_color=CORES["texto"],
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )
        titulo.pack()

        subtitulo = ctk.CTkLabel(
            container,
            text=DESCRIPTION,
            text_color=CORES["texto_secundario"],
            font=ctk.CTkFont(size=13)
        )
        subtitulo.pack(
            pady=(6, 6)
        )

        versao = ctk.CTkLabel(
            container,
            text=f"v{VERSION}",
            text_color=CORES["texto_secundario"],
            font=ctk.CTkFont(size=12)
        )
        versao.pack(
            pady=(0, 18)
        )

        self.barra = ctk.CTkProgressBar(
            container,
            width=320,
            height=10,
            corner_radius=8,
            progress_color=CORES["roxo"],
            fg_color=CORES["borda"]
        )
        self.barra.pack(
            pady=(0, 12)
        )
        self.barra.set(0)

        self.status = ctk.CTkLabel(
            container,
            text="Inicializando...",
            text_color=CORES["texto_secundario"],
            font=ctk.CTkFont(size=12)
        )
        self.status.pack()

        self.progresso = 0
        self.animar_barra()

    def animar_barra(self):
        if self.progresso >= 1:
            self.fechar()
            return

        self.progresso += 0.03
        self.barra.set(self.progresso)

        if self.progresso < 0.35:
            self.status.configure(
                text="Carregando interface..."
            )
        elif self.progresso < 0.70:
            self.status.configure(
                text="Preparando componentes..."
            )
        else:
            self.status.configure(
                text="Quase pronto..."
            )

        intervalo = max(
            15,
            int(self.duracao_ms * 0.03)
        )

        self.after(
            intervalo,
            self.animar_barra
        )

    def fechar(self):
        self.destroy()

        self.master.deiconify()
        self.master.lift()
        self.master.focus_force()