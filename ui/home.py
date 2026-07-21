import os
import threading
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from config.config import EORDER_URL
from core.executor import BotEorderExecutor
from ui.components.header import PageHeader
from ui.components.stat_card import StatCard
from datetime import datetime
from ui.theme import CORES


class HomePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color=CORES["fundo"]
        )

        self.executor = None
        self.thread_execucao = None
        self.caminho_relatorio = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.criar_header()
        self.criar_card_planilha()
        self.criar_cards_estatisticas()
        self.criar_painel_logs()
        self.criar_acoes()

    # =========================================================
    # INTERFACE
    # =========================================================

    def criar_header(self):
        self.header = PageHeader(
            self,
            titulo="Bot eOrder",
            subtitulo=(
                "Automação Inteligente de "
                "Cancelamento de TdCs"
            )
        )

        self.header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=30,
            pady=(25, 15)
        )

    def criar_card_planilha(self):
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
            sticky="ew",
            padx=30,
            pady=(0, 15)
        )

        card.grid_columnconfigure(0, weight=1)

        titulo = ctk.CTkLabel(
            card,
            text="Planilha de entrada",
            text_color=CORES["texto"],
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )
        titulo.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(18, 8)
        )

        self.entry_planilha = ctk.CTkEntry(
            card,
            placeholder_text="Nenhuma planilha selecionada...",
            height=42
        )
        self.entry_planilha.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(20, 10),
            pady=(0, 18)
        )

        self.botao_selecionar = ctk.CTkButton(
            card,
            text="Selecionar",
            width=105,
            height=42,
            fg_color=CORES["azul"],
            hover_color=CORES["azul_hover"],
            command=self.selecionar_planilha
        )
        self.botao_selecionar.grid(
            row=1,
            column=1,
            padx=(0, 20),
            pady=(0, 18)
        )

    def criar_cards_estatisticas(self):
        container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        container.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=30,
            pady=(0, 10)
        )

        for coluna in range(4):
            container.grid_columnconfigure(
                coluna,
                weight=1
            )

        self.card_canceladas = StatCard(
            container,
            titulo="Canceladas",
            icone="✔",
            cor_destaque=CORES["verde"]
        )
        self.card_canceladas.grid(
            row=0,
            column=0,
            padx=6,
            sticky="ew"
        )

        self.card_anuladas = StatCard(
            container,
            titulo="Já anuladas",
            icone="⚠",
            cor_destaque=CORES["amarelo"]
        )
        self.card_anuladas.grid(
            row=0,
            column=1,
            padx=6,
            sticky="ew"
        )

        self.card_finalizadas = StatCard(
            container,
            titulo="WO Finalizadas",
            icone="📦",
            cor_destaque=CORES["azul"]
        )
        self.card_finalizadas.grid(
            row=0,
            column=2,
            padx=6,
            sticky="ew"
        )

        self.card_erros = StatCard(
            container,
            titulo="Erros",
            icone="✖",
            cor_destaque=CORES["vermelho"]
        )
        self.card_erros.grid(
            row=0,
            column=3,
            padx=6,
            sticky="ew"
        )

    def criar_painel_logs(self):
        card = ctk.CTkFrame(
            self,
            corner_radius=16,
            fg_color=CORES["card"],
            border_width=1,
            border_color=CORES["borda"]
        )
        card.grid(
            row=3,
            column=0,
            sticky="nsew",
            padx=30,
            pady=(0, 12)
        )

        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(3, weight=1)

        topo = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )
        topo.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=20,
            pady=(16, 8)
        )

        titulo = ctk.CTkLabel(
            topo,
            text="Logs da execução",
            text_color=CORES["texto"],
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )
        titulo.pack(side="left")

        self.label_status = ctk.CTkLabel(
            topo,
            text="● Pronto",
            text_color=CORES["verde"],
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )
        self.label_status.pack(side="right")

        self.label_progresso = ctk.CTkLabel(
            card,
            text="0 / 0",
            text_color=CORES["texto_secundario"]
        )
        self.label_progresso.grid(
            row=1,
            column=0,
            sticky="e",
            padx=20
        )

        self.barra_progresso = ctk.CTkProgressBar(
            card,
            height=12,
            corner_radius=8,
            progress_color=CORES["roxo"],
            fg_color=CORES["borda"]
        )
        self.barra_progresso.set(0)
        self.barra_progresso.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=20,
            pady=(4, 10)
        )

        self.textbox_logs = ctk.CTkTextbox(
            card,
            corner_radius=10,
            fg_color=CORES["fundo"],
            text_color=CORES["texto"],
            border_width=1,
            border_color=CORES["borda"],
            font=ctk.CTkFont(
                family="Consolas",
                size=12
            )
        )
        self.textbox_logs.grid(
            row=3,
            column=0,
            sticky="nsew",
            padx=20,
            pady=(0, 20)
        )

        self.textbox_logs.insert(
            "end",
            "Aguardando execução...\n"
        )
        self.textbox_logs.configure(
            state="disabled"
        )

    def criar_acoes(self):
        container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        container.grid(
            row=4,
            column=0,
            sticky="ew",
            padx=30,
            pady=(0, 25)
        )

        self.botao_iniciar = ctk.CTkButton(
            container,
            text="Iniciar",
            height=44,
            width=130,
            fg_color=CORES["roxo"],
            hover_color=CORES["roxo_hover"],
            command=self.iniciar_execucao
        )
        self.botao_iniciar.pack(
            side="left",
            padx=(0, 10)
        )

        self.botao_parar = ctk.CTkButton(
            container,
            text="Parar",
            height=44,
            width=130,
            state="disabled",
            fg_color=CORES["vermelho"],
            hover_color="#B92626",
            command=self.parar_execucao
        )
        self.botao_parar.pack(
            side="left",
            padx=(0, 10)
        )

        self.botao_relatorio = ctk.CTkButton(
            container,
            text="📂 Abrir relatório",
            height=44,
            width=150,
            state="disabled",
            fg_color="transparent",
            hover_color=CORES["card_hover"],
            border_width=1,
            border_color=CORES["borda"],
            command=self.abrir_relatorio
        )
        self.botao_relatorio.pack(
            side="right"
        )

    # =========================================================
    # PLANILHA
    # =========================================================

    def selecionar_planilha(self):
        caminho = filedialog.askopenfilename(
            title="Selecione a planilha",
            filetypes=[
                ("Planilhas Excel", "*.xlsx"),
                ("Todos os arquivos", "*.*")
            ]
        )

        if not caminho:
            return

        self.entry_planilha.delete(0, "end")
        self.entry_planilha.insert(0, caminho)

        self.adicionar_log(
            f"Planilha selecionada: {caminho}"
        )

    # =========================================================
    # EXECUÇÃO
    # =========================================================

    def iniciar_execucao(self):
        caminho_planilha = (
            self.entry_planilha.get().strip()
        )

        if not caminho_planilha:
            messagebox.showwarning(
                "Planilha não selecionada",
                "Selecione uma planilha antes de iniciar."
            )
            return

        if not Path(caminho_planilha).exists():
            messagebox.showerror(
                "Arquivo não encontrado",
                "A planilha selecionada não existe."
            )
            return

        if (
            self.thread_execucao
            and self.thread_execucao.is_alive()
        ):
            messagebox.showwarning(
                "Execução em andamento",
                "O bot já está em execução."
            )
            return

        self.limpar_interface_execucao()

        self.alterar_status(
            "● Iniciando...",
            CORES["amarelo"]
        )

        self.botao_iniciar.configure(
            state="disabled"
        )
        self.botao_selecionar.configure(
            state="disabled"
        )
        self.botao_parar.configure(
            state="normal"
        )
        self.botao_relatorio.configure(
            state="disabled"
        )

        self.executor = BotEorderExecutor(
            eorder_url=EORDER_URL,
            excel_path=caminho_planilha,
            callback_log=self.callback_log,
            callback_progresso=self.callback_progresso,
            callback_login=self.callback_login
        )

        self.thread_execucao = threading.Thread(
            target=self.executar_em_background,
            daemon=True
        )
        self.thread_execucao.start()

    def executar_em_background(self):
        try:
            self.executor.executar()

            self.caminho_relatorio = (
                self.executor.caminho_relatorio
            )

            if self.executor.evento_parar.is_set():
                self.after(
                    0,
                    lambda: self.alterar_status(
                        "● Interrompido",
                        CORES["vermelho"]
                    )
                )

            else:
                self.after(
                    0,
                    lambda: self.alterar_status(
                        "● Finalizado",
                        CORES["verde"]
                    )
                )

                self.after(
                    0,
                    lambda: messagebox.showinfo(
                        "Execução finalizada",
                        "O processamento foi concluído."
                    )
                )

        except Exception as erro:
            self.callback_log(
                f"Erro crítico na interface: {erro}"
            )

            self.after(
                0,
                lambda: self.alterar_status(
                    "● Erro",
                    CORES["vermelho"]
                )
            )

            self.after(
                0,
                lambda erro=erro: messagebox.showerror(
                    "Erro na execução",
                    str(erro)
                )
            )

        finally:
            self.after(
                0,
                self.finalizar_estado_interface
            )

    def parar_execucao(self):
        if not self.executor:
            return

        confirmar = messagebox.askyesno(
            "Interromper execução",
            "Deseja realmente parar o robô?"
        )

        if not confirmar:
            return

        self.executor.parar()

        self.alterar_status(
            "● Parando...",
            CORES["amarelo"]
        )

        self.botao_parar.configure(
            state="disabled"
        )

    # =========================================================
    # CALLBACKS
    # =========================================================

    def callback_log(self, mensagem: str):
        self.after(
            0,
            lambda: self.adicionar_log(mensagem)
        )

    def callback_progresso(
        self,
        processadas,
        total,
        estatisticas
    ):
        self.after(
            0,
            lambda: self.atualizar_progresso(
                processadas,
                total,
                estatisticas
            )
        )

    def callback_login(self):
        evento_confirmacao = threading.Event()

        def exibir_dialogo():
            self.alterar_status(
                "● Aguardando login",
                CORES["amarelo"]
            )

            messagebox.showinfo(
                "Login necessário",
                (
                    "O navegador foi aberto.\n\n"
                    "Faça login no eOrder e navegue até "
                    "o Menu Principal.\n\n"
                    "Depois clique em OK para continuar."
                )
            )

            evento_confirmacao.set()

        self.after(
            0,
            exibir_dialogo
        )

        evento_confirmacao.wait()

        self.after(
            0,
            lambda: self.alterar_status(
                "● Processando",
                CORES["azul"]
            )
        )

    # =========================================================
    # ATUALIZAÇÕES VISUAIS
    # =========================================================

    def adicionar_log(self, mensagem: str):
        horario = datetime.now().strftime("%H:%M:%S")
        self.textbox_logs.configure(
            state="normal"
        )

        self.textbox_logs.insert(
            "end",
            f"[{horario}]{mensagem}\n"
        )

        self.textbox_logs.see("end")

        self.textbox_logs.configure(
            state="disabled"
        )

    def atualizar_progresso(
        self,
        processadas,
        total,
        estatisticas
    ):
        progresso = (
            processadas / total
            if total > 0
            else 0
        )

        self.barra_progresso.set(
            progresso
        )

        self.label_progresso.configure(
            text=f"{processadas} / {total}"
        )

        self.card_canceladas.atualizar_valor(
            estatisticas.canceladas
        )

        self.card_anuladas.atualizar_valor(
            estatisticas.ja_anuladas
        )

        self.card_finalizadas.atualizar_valor(
            estatisticas.wo_finalizadas
        )

        self.card_erros.atualizar_valor(
            estatisticas.erros
        )

    def alterar_status(self, texto, cor):
        self.label_status.configure(
            text=texto,
            text_color=cor
        )

    def limpar_interface_execucao(self):
        self.caminho_relatorio = None

        self.card_canceladas.atualizar_valor(0)
        self.card_anuladas.atualizar_valor(0)
        self.card_finalizadas.atualizar_valor(0)
        self.card_erros.atualizar_valor(0)

        self.barra_progresso.set(0)

        self.label_progresso.configure(
            text="0 / 0"
        )

        self.textbox_logs.configure(
            state="normal"
        )

        self.textbox_logs.delete(
            "1.0",
            "end"
        )

        self.textbox_logs.insert(
            "end",
            "Iniciando execução...\n"
        )

        self.textbox_logs.configure(
            state="disabled"
        )

    def finalizar_estado_interface(self):
        self.botao_iniciar.configure(
            state="normal"
        )

        self.botao_selecionar.configure(
            state="normal"
        )

        self.botao_parar.configure(
            state="disabled"
        )

        if (
            self.caminho_relatorio
            and Path(self.caminho_relatorio).exists()
        ):
            self.botao_relatorio.configure(
                state="normal"
            )

    # =========================================================
    # RELATÓRIO
    # =========================================================

    def abrir_relatorio(self):
        if not self.caminho_relatorio:
            messagebox.showwarning(
                "Relatório indisponível",
                "Nenhum relatório foi gerado."
            )
            return

        caminho = Path(
            self.caminho_relatorio
        )

        if not caminho.exists():
            messagebox.showerror(
                "Arquivo não encontrado",
                "O relatório não foi encontrado."
            )
            return

        try:
            os.startfile(
                str(caminho)
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro ao abrir relatório",
                str(erro)
            )