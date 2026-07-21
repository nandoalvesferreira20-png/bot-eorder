from datetime import datetime
from threading import Event
from typing import Callable, Optional

from browser.navegador import abrir_eorder
from eorder.busca import abrir_busca_tdcs
from eorder.cancelamento import processar_tdc
from excel.leitor_excel import ler_notas_excel
from utils.estatisticas import EstatisticasExecucao
from utils.logger import configurar_logger
from utils.relatorio import gerar_relatorio_excel
from utils.screenshots import salvar_screenshot_erro


LogCallback = Callable[[str], None]
ProgressoCallback = Callable[[int, int, EstatisticasExecucao], None]
LoginCallback = Callable[[], None]


def callback_vazio(*args, **kwargs):
    """Callback padrão para execução sem interface."""
    return None


class BotEorderExecutor:
    def __init__(
        self,
        eorder_url: str,
        excel_path: str,
        callback_log: Optional[LogCallback] = None,
        callback_progresso: Optional[ProgressoCallback] = None,
        callback_login: Optional[LoginCallback] = None,
        evento_parar: Optional[Event] = None
    ):
        self.eorder_url = eorder_url
        self.excel_path = excel_path

        self.callback_log = callback_log or callback_vazio
        self.callback_progresso = (
            callback_progresso or callback_vazio
        )
        self.callback_login = callback_login or callback_vazio
        self.evento_parar = evento_parar or Event()

        self.logger = None
        self.caminho_log = None
        self.identificador_execucao = None

        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.frame = None

        self.estatisticas = None
        self.caminho_relatorio = None

    def log(self, mensagem: str, nivel: str = "info"):
        self.callback_log(mensagem)

        if not self.logger:
            return

        metodo = getattr(self.logger, nivel, self.logger.info)
        metodo(mensagem)

    def reiniciar_fluxo(self):
        self.log(
            "Reiniciando o fluxo do eOrder...",
            "warning"
        )

        self.page.reload(
            wait_until="domcontentloaded",
            timeout=60000
        )

        self.frame = self.page.frame_locator(
            'iframe[name="mainFrame"]'
        )

        self.frame.get_by_text(
            "Menu Principal"
        ).wait_for(timeout=60000)

        abrir_busca_tdcs(self.frame)

        self.log("Fluxo reiniciado com sucesso.")

    def registrar_resultado(
        self,
        indice: int,
        total: int,
        centro_operativo: str,
        codigo_externo: str,
        resultado: str
    ):
        if resultado == "JA_ANULADA":
            mensagem = "TdC já estava anulada."

            self.log(
                f"[{indice}/{total}] PULADA - "
                f"{codigo_externo} já estava anulada",
                "warning"
            )

        elif resultado == "WO_FINALIZADA":
            mensagem = "WO possui status finalizado."

            self.log(
                f"[{indice}/{total}] PULADA - "
                f"{codigo_externo} possui WO finalizada",
                "warning"
            )

        else:
            resultado = "CANCELADA"
            mensagem = "Cancelamento concluído."

            self.log(
                f"[{indice}/{total}] OK - "
                f"{codigo_externo}"
            )

        self.estatisticas.registrar(
            centro_operativo=centro_operativo,
            codigo_externo=codigo_externo,
            resultado=resultado,
            mensagem=mensagem
        )

        self.callback_progresso(
            indice,
            total,
            self.estatisticas
        )

    def registrar_erro(
        self,
        indice: int,
        total: int,
        centro_operativo: str,
        codigo_externo: str,
        erro: Exception
    ):
        mensagem_erro = str(erro)

        self.estatisticas.registrar(
            centro_operativo=centro_operativo,
            codigo_externo=codigo_externo,
            resultado="ERRO",
            mensagem=mensagem_erro
        )

        self.log(
            f"[{indice}/{total}] ERRO - "
            f"{codigo_externo}: {mensagem_erro}",
            "error"
        )

        self.callback_progresso(
            indice,
            total,
            self.estatisticas
        )

    def salvar_screenshot(
        self,
        codigo_externo: str
    ):
        if not self.page:
            return None

        try:
            caminho = salvar_screenshot_erro(
                page=self.page,
                codigo_externo=codigo_externo,
                identificador_execucao=(
                    self.identificador_execucao
                )
            )

            self.log(
                f"Screenshot salvo em: {caminho}"
            )

            return caminho

        except Exception as erro:
            self.log(
                f"Falha ao salvar screenshot: {erro}",
                "error"
            )

            return None

    def executar(self):
        inicio_execucao = datetime.now()

        (
            self.logger,
            self.caminho_log,
            self.identificador_execucao
        ) = configurar_logger()

        notas = ler_notas_excel(self.excel_path)

        self.estatisticas = EstatisticasExecucao(
            total=len(notas)
        )

        self.log(
            f"Notas carregadas: {len(notas)}"
        )

        if not notas:
            self.log(
                "Nenhuma nota encontrada.",
                "warning"
            )
            return self.estatisticas

        try:
            (
                self.playwright,
                self.browser,
                self.context,
                self.page
            ) = abrir_eorder(self.eorder_url)

            self.log(
                "Navegador aberto. Realize o login."
            )

            # Na GUI, este callback abrirá uma janela pedindo
            # confirmação. No terminal, usaremos input().
            self.callback_login()

            self.frame = self.page.frame_locator(
                'iframe[name="mainFrame"]'
            )

            self.frame.get_by_text(
                "Menu Principal"
            ).wait_for(timeout=30000)

            total = len(notas)

            for indice, nota in enumerate(
                notas,
                start=1
            ):
                if self.evento_parar.is_set():
                    self.log(
                        "Execução interrompida pelo usuário.",
                        "warning"
                    )
                    break

                centro_operativo = str(
                    nota["centro_operativo"]
                ).strip()

                codigo_externo = str(
                    nota["codigo_externo"]
                ).strip()

                self.log(
                    f"[{indice}/{total}] Iniciando "
                    f"{codigo_externo}"
                )

                tentativa = 1
                max_tentativas = 2
                concluida = False

                while tentativa <= max_tentativas:
                    if self.evento_parar.is_set():
                        break

                    try:
                        abrir_busca_tdcs(self.frame)

                        resultado = processar_tdc(
                            self.frame,
                            centro_operativo=centro_operativo,
                            codigo_externo=codigo_externo
                        )

                        self.registrar_resultado(
                            indice=indice,
                            total=total,
                            centro_operativo=(
                                centro_operativo
                            ),
                            codigo_externo=codigo_externo,
                            resultado=resultado
                        )

                        concluida = True
                        break

                    except Exception as erro:
                        mensagem_erro = str(erro)

                        self.log(
                            f"Erro na tentativa "
                            f"{tentativa}/{max_tentativas}: "
                            f"{mensagem_erro}",
                            "error"
                        )

                        self.salvar_screenshot(
                            codigo_externo
                        )

                        erro_filtros = (
                            'name="filtros"'
                            in mensagem_erro
                            or
                            "Não foi possível abrir os filtros"
                            in mensagem_erro
                        )

                        if (
                            erro_filtros
                            and tentativa < max_tentativas
                        ):
                            self.reiniciar_fluxo()
                            tentativa += 1
                            continue

                        self.registrar_erro(
                            indice=indice,
                            total=total,
                            centro_operativo=(
                                centro_operativo
                            ),
                            codigo_externo=codigo_externo,
                            erro=erro
                        )

                        break

                if not concluida:
                    self.log(
                        f"TdC encerrada sem sucesso: "
                        f"{codigo_externo}",
                        "warning"
                    )

            self.log(
                "Processamento da planilha concluído."
            )

            return self.estatisticas

        except Exception as erro:
            self.log(
                f"Erro crítico: {erro}",
                "error"
            )

            self.salvar_screenshot("ERRO_CRITICO")
            raise

        finally:
            fim_execucao = datetime.now()

            try:
                self.caminho_relatorio = (
                    gerar_relatorio_excel(
                        estatisticas=self.estatisticas,
                        identificador_execucao=(
                            self.identificador_execucao
                        ),
                        inicio_execucao=inicio_execucao,
                        fim_execucao=fim_execucao
                    )
                )

                self.log(
                    f"Relatório salvo em: "
                    f"{self.caminho_relatorio}"
                )

            except Exception as erro:
                self.log(
                    f"Falha ao gerar relatório: {erro}",
                    "error"
                )

            self.fechar()

    def fechar(self):
        try:
            if self.context:
                self.context.close()
        except Exception:
            pass

        try:
            if self.browser:
                self.browser.close()
        except Exception:
            pass

        try:
            if self.playwright:
                self.playwright.stop()
        except Exception:
            pass

    def parar(self):
        self.evento_parar.set()
        self.log(
            "Solicitação de parada recebida.",
            "warning"
        )