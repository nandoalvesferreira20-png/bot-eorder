import os
import threading
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from config.config import EORDER_URL
from core.executor import BotEorderExecutor


class HomePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color="transparent"
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
    # CONSTRUÇÃO DA INTERFACE
    # =========================================================

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
            text="Painel de execução",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )
        titulo.pack(anchor="w")

        subtitulo = ctk.CTkLabel(
            header,
            text=(
                "Acompanhe o processamento "
                "das TdCs em tempo real."
            ),
            text_color="gray70",
            font=ctk.CTkFont(size=14)
        )
        subtitulo.pack(
            anchor="w",
            pady=(4, 0)
        )

    def criar_card_planilha(self):
        card = ctk.CTkFrame(
            self,
            corner_radius=14
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
            placeholder_text="Selecione o arquivo Excel",
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
            width=120,
            height=42,
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
            pady=(0, 15)
        )

        for coluna in range(4):
            container.grid_columnconfigure(
                coluna,
                weight=1
            )

        self.card_canceladas = self.criar_card_estatistica(
            container,
            coluna=0,
            titulo="Canceladas"
        )

        self.card_anuladas = self.criar_card_estatistica(
            container,
            coluna=1,
            titulo="Já anuladas"
        )

        self.card_finalizadas = self.criar_card_estatistica(
            container,
            coluna=2,
            titulo="WO finalizadas"
        )

        self.card_erros = self.criar_card_estatistica(
            container,
            coluna=3,
            titulo="Erros"
        )

    def criar_card_estatistica(
        self,
        master,
        coluna,
        titulo
    ):
        card = ctk.CTkFrame(
            master,
            corner_radius=14
        )
        card.grid(
            row=0,
            column=coluna,
            sticky="ew",
            padx=6
        )

        label_titulo = ctk.CTkLabel(
            card,
            text=titulo,
            text_color="gray70",
            font=ctk.CTkFont(size=13)
        )
        label_titulo.pack(
            anchor="w",
            padx=18,
            pady=(15, 4)
        )

        label_valor = ctk.CTkLabel(
            card,
            text="0",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )
        label_valor.pack(
            anchor="w",
            padx=18,
            pady=(0, 15)
        )

        return label_valor

    def criar_painel_logs(self):
        card = ctk.CTkFrame(
            self,
            corner_radius=14
        )
        card.grid(
            row=3,
            column=0,
            sticky="nsew",
            padx=30,
            pady=(0, 15)
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
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )
        titulo.pack(side="left")

        self.label_status = ctk.CTkLabel(
            topo,
            text="● Pronto",
            text_color="#40C057",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )
        self.label_status.pack(side="right")

        self.label_progresso = ctk.CTkLabel(
            card,
            text="0 / 0",
            text_color="gray70"
        )
        self.label_progresso.grid(
            row=1,
            column=0,
            sticky="e",
            padx=20
        )

        self.barra_progresso = ctk.CTkProgressBar(card)
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
            fg_color="#C92A2A",
            hover_color="#A51111",
            command=self.parar_execucao
        )
        self.botao_parar.pack(
            side="left",
            padx=(0, 10)
        )

        self.botao_relatorio = ctk.CTkButton(
            container,
            text="Abrir relatório",
            height=44,
            width=150,
            state="disabled",
            fg_color="transparent",
            border_width=1,
            command=self.abrir_relatorio
        )
        self.botao_relatorio.pack(side="right")

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
        caminho_planilha = self.entry_planilha.get().strip()

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
            "#FAB005"
        )

        self.botao_iniciar.configure(state="disabled")
        self.botao_selecionar.configure(state="disabled")
        self.botao_parar.configure(state="normal")
        self.botao_relatorio.configure(state="disabled")

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
                        "#FA5252"
                    )
                )
            else:
                self.after(
                    0,
                    lambda: self.alterar_status(
                        "● Finalizado",
                        "#40C057"
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
                    "#FA5252"
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
            "#FAB005"
        )

        self.botao_parar.configure(state="disabled")

    # =========================================================
    # CALLBACKS DO EXECUTOR
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
                "#FAB005"
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

        self.after(0, exibir_dialogo)

        # Mantém a thread do robô aguardando,
        # sem congelar a interface.
        evento_confirmacao.wait()

        self.after(
            0,
            lambda: self.alterar_status(
                "● Processando",
                "#339AF0"
            )
        )

    # =========================================================
    # ATUALIZAÇÕES VISUAIS
    # =========================================================

    def adicionar_log(self, mensagem: str):
        self.textbox_logs.configure(state="normal")
        self.textbox_logs.insert(
            "end",
            f"{mensagem}\n"
        )
        self.textbox_logs.see("end")
        self.textbox_logs.configure(state="disabled")

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

        self.barra_progresso.set(progresso)

        self.label_progresso.configure(
            text=f"{processadas} / {total}"
        )

        self.card_canceladas.configure(
            text=str(estatisticas.canceladas)
        )
        self.card_anuladas.configure(
            text=str(estatisticas.ja_anuladas)
        )
        self.card_finalizadas.configure(
            text=str(estatisticas.wo_finalizadas)
        )
        self.card_erros.configure(
            text=str(estatisticas.erros)
        )

    def alterar_status(
        self,
        texto,
        cor
    ):
        self.label_status.configure(
            text=texto,
            text_color=cor
        )

    def limpar_interface_execucao(self):
        self.caminho_relatorio = None

        self.card_canceladas.configure(text="0")
        self.card_anuladas.configure(text="0")
        self.card_finalizadas.configure(text="0")
        self.card_erros.configure(text="0")

        self.barra_progresso.set(0)
        self.label_progresso.configure(text="0 / 0")

        self.textbox_logs.configure(state="normal")
        self.textbox_logs.delete("1.0", "end")
        self.textbox_logs.insert(
            "end",
            "Iniciando execução...\n"
        )
        self.textbox_logs.configure(state="disabled")

    def finalizar_estado_interface(self):
        self.botao_iniciar.configure(state="normal")
        self.botao_selecionar.configure(state="normal")
        self.botao_parar.configure(state="disabled")

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

        caminho = Path(self.caminho_relatorio)

        if not caminho.exists():
            messagebox.showerror(
                "Arquivo não encontrado",
                "O relatório não foi encontrado."
            )
            return

        try:
            os.startfile(str(caminho))

        except Exception as erro:
            messagebox.showerror(
                "Erro ao abrir relatório",
                str(erro)
            )