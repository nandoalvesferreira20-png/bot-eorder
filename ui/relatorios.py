import os
from pathlib import Path
from tkinter import messagebox

import customtkinter as ctk


class RelatoriosPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color="transparent"
        )

        self.pasta_relatorios = Path("relatorios")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.criar_header()
        self.criar_lista_relatorios()
        self.atualizar_lista()

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
            text="Relatórios",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )
        titulo.pack(anchor="w")

        subtitulo = ctk.CTkLabel(
            header,
            text=(
                "Consulte os relatórios gerados "
                "nas execuções anteriores."
            ),
            text_color="gray70",
            font=ctk.CTkFont(size=14)
        )
        subtitulo.pack(
            anchor="w",
            pady=(4, 0)
        )

        botao_atualizar = ctk.CTkButton(
            header,
            text="Atualizar",
            width=110,
            command=self.atualizar_lista
        )
        botao_atualizar.pack(
            side="right",
            pady=(0, 5)
        )

    def criar_lista_relatorios(self):
        self.card_lista = ctk.CTkScrollableFrame(
            self,
            corner_radius=14,
            label_text="Arquivos disponíveis"
        )
        self.card_lista.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=30,
            pady=(0, 25)
        )

        self.card_lista.grid_columnconfigure(
            0,
            weight=1
        )

    def limpar_lista(self):
        for widget in self.card_lista.winfo_children():
            widget.destroy()

    def atualizar_lista(self):
        self.limpar_lista()

        self.pasta_relatorios.mkdir(
            parents=True,
            exist_ok=True
        )

        arquivos = sorted(
            self.pasta_relatorios.glob("*.xlsx"),
            key=lambda arquivo: arquivo.stat().st_mtime,
            reverse=True
        )

        if not arquivos:
            mensagem = ctk.CTkLabel(
                self.card_lista,
                text="Nenhum relatório encontrado.",
                text_color="gray70",
                font=ctk.CTkFont(size=14)
            )
            mensagem.grid(
                row=0,
                column=0,
                pady=30
            )
            return

        for indice, arquivo in enumerate(arquivos):
            self.criar_item_relatorio(
                arquivo,
                indice
            )

    def criar_item_relatorio(
        self,
        arquivo: Path,
        linha: int
    ):
        item = ctk.CTkFrame(
            self.card_lista,
            corner_radius=12
        )
        item.grid(
            row=linha,
            column=0,
            sticky="ew",
            padx=4,
            pady=6
        )

        item.grid_columnconfigure(
            0,
            weight=1
        )

        nome = ctk.CTkLabel(
            item,
            text=arquivo.name,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )
        nome.grid(
            row=0,
            column=0,
            sticky="w",
            padx=16,
            pady=(13, 2)
        )

        data_modificacao = (
            arquivo.stat().st_mtime
        )

        from datetime import datetime

        data_formatada = datetime.fromtimestamp(
            data_modificacao
        ).strftime("%d/%m/%Y %H:%M:%S")

        info = ctk.CTkLabel(
            item,
            text=f"Gerado em: {data_formatada}",
            text_color="gray70",
            font=ctk.CTkFont(size=12)
        )
        info.grid(
            row=1,
            column=0,
            sticky="w",
            padx=16,
            pady=(0, 13)
        )

        botao_abrir = ctk.CTkButton(
            item,
            text="Abrir",
            width=90,
            command=lambda caminho=arquivo: (
                self.abrir_relatorio(caminho)
            )
        )
        botao_abrir.grid(
            row=0,
            column=1,
            rowspan=2,
            padx=16,
            pady=12
        )

    def abrir_relatorio(self, caminho: Path):
        try:
            os.startfile(str(caminho.resolve()))

        except Exception as erro:
            messagebox.showerror(
                "Erro ao abrir relatório",
                str(erro)
            )