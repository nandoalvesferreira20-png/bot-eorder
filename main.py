from datetime import datetime

from config.config import EORDER_URL, EXCEL_PATH
from excel.leitor_excel import ler_notas_excel
from browser.navegador import abrir_eorder
from eorder.busca import abrir_busca_tdcs
from eorder.cancelamento import processar_tdc
from utils.logger import configurar_logger
from utils.estatisticas import EstatisticasExecucao
from utils.screenshots import salvar_screenshot_erro
from utils.relatorio import gerar_relatorio_excel


def reiniciar_fluxo(page, logger):
    logger.warning("Reiniciando o fluxo do eOrder.")

    page.reload(
        wait_until="domcontentloaded",
        timeout=60000
    )

    frame = page.frame_locator(
        'iframe[name="mainFrame"]'
    )

    frame.get_by_text("Menu Principal").wait_for(
        timeout=60000
    )

    abrir_busca_tdcs(frame)

    logger.info("Fluxo reiniciado com sucesso.")

    return frame


def registrar_resultado(
    estatisticas,
    logger,
    indice,
    total,
    centro_operativo,
    codigo_externo,
    resultado
):
    if resultado == "JA_ANULADA":
        mensagem = "TdC já estava anulada."

        print(
            f"[{indice}/{total}] PULADA - "
            f"{codigo_externo} já estava anulada"
        )

        logger.warning(
            f"JA_ANULADA | Centro: {centro_operativo} | "
            f"TdC: {codigo_externo}"
        )

    elif resultado == "WO_FINALIZADA":
        mensagem = "WO possui status finalizado."

        print(
            f"[{indice}/{total}] PULADA - "
            f"{codigo_externo} possui WO finalizada"
        )

        logger.warning(
            f"WO_FINALIZADA | Centro: {centro_operativo} | "
            f"TdC: {codigo_externo}"
        )

    else:
        resultado = "CANCELADA"
        mensagem = "Cancelamento concluído."

        print(
            f"[{indice}/{total}] OK - "
            f"{codigo_externo}"
        )

        logger.info(
            f"CANCELADA | Centro: {centro_operativo} | "
            f"TdC: {codigo_externo}"
        )

    estatisticas.registrar(
        centro_operativo=centro_operativo,
        codigo_externo=codigo_externo,
        resultado=resultado,
        mensagem=mensagem
    )


def main():
    inicio_execucao = datetime.now()

    logger, caminho_log, identificador_execucao = (
        configurar_logger()
    )

    logger.info("Execução do Bot eOrder iniciada.")

    notas = ler_notas_excel(EXCEL_PATH)

    print(f"Notas carregadas: {len(notas)}")
    logger.info(f"Notas carregadas: {len(notas)}")

    if not notas:
        print("Nenhuma nota encontrada.")
        logger.warning("Nenhuma nota encontrada.")
        return

    estatisticas = EstatisticasExecucao(
        total=len(notas)
    )

    playwright = None
    browser = None
    context = None
    page = None

    try:
        playwright, browser, context, page = abrir_eorder(
            EORDER_URL
        )

        input(
            "Faça login no eOrder e aperte ENTER "
            "aqui no terminal para continuar..."
        )

        logger.info("Login manual confirmado pelo usuário.")

        frame = page.frame_locator(
            'iframe[name="mainFrame"]'
        )

        frame.get_by_text("Menu Principal").wait_for(
            timeout=30000
        )

        total_notas = len(notas)

        for indice, nota in enumerate(notas, start=1):
            centro_operativo = str(
                nota["centro_operativo"]
            ).strip()

            codigo_externo = str(
                nota["codigo_externo"]
            ).strip()

            print(
                f"\n[{indice}/{total_notas}] "
                f"Iniciando {codigo_externo}"
            )

            logger.info(
                f"INICIANDO | Linha: {indice}/{total_notas} | "
                f"Centro: {centro_operativo} | "
                f"TdC: {codigo_externo}"
            )

            tentativa = 1
            max_tentativas = 2
            nota_concluida = False

            while tentativa <= max_tentativas:
                try:
                    abrir_busca_tdcs(frame)

                    resultado = processar_tdc(
                        frame,
                        centro_operativo=centro_operativo,
                        codigo_externo=codigo_externo
                    )

                    registrar_resultado(
                        estatisticas=estatisticas,
                        logger=logger,
                        indice=indice,
                        total=total_notas,
                        centro_operativo=centro_operativo,
                        codigo_externo=codigo_externo,
                        resultado=resultado
                    )

                    nota_concluida = True
                    break

                except Exception as erro:
                    mensagem_erro = str(erro)

                    logger.exception(
                        f"ERRO NA TENTATIVA {tentativa}/"
                        f"{max_tentativas} | "
                        f"Centro: {centro_operativo} | "
                        f"TdC: {codigo_externo}"
                    )

                    print(
                        f"\nErro na tentativa "
                        f"{tentativa}/{max_tentativas}"
                    )
                    print(f"TdC: {codigo_externo}")
                    print(f"Motivo: {erro}")

                    try:
                        caminho_screenshot = (
                            salvar_screenshot_erro(
                                page=page,
                                codigo_externo=codigo_externo,
                                identificador_execucao=(
                                    identificador_execucao
                                )
                            )
                        )

                        logger.info(
                            "Screenshot do erro salvo em: "
                            f"{caminho_screenshot}"
                        )

                    except Exception as erro_screenshot:
                        logger.error(
                            "Falha ao salvar screenshot: "
                            f"{erro_screenshot}"
                        )

                    erro_filtros = (
                        'name="filtros"' in mensagem_erro
                        or
                        "Não foi possível abrir os filtros"
                        in mensagem_erro
                    )

                    if (
                        erro_filtros
                        and tentativa < max_tentativas
                    ):
                        logger.warning(
                            "Erro ao abrir os filtros. "
                            "A mesma TdC será processada novamente."
                        )

                        frame = reiniciar_fluxo(
                            page,
                            logger
                        )

                        tentativa += 1
                        continue

                    estatisticas.registrar(
                        centro_operativo=centro_operativo,
                        codigo_externo=codigo_externo,
                        resultado="ERRO",
                        mensagem=mensagem_erro
                    )

                    print(
                        "\nNão foi possível recuperar "
                        "automaticamente."
                    )

                    input(
                        "Ajuste o eOrder manualmente para "
                        "Busca TdCs e aperte ENTER para "
                        "seguir para a próxima nota..."
                    )

                    break

            if not nota_concluida:
                logger.warning(
                    f"TdC encerrada com erro: {codigo_externo}"
                )

        print("\nProcessamento da planilha concluído.")
        logger.info("Processamento da planilha concluído.")

    except Exception:
        logger.exception(
            "Erro crítico durante a execução do bot."
        )

        if page:
            try:
                salvar_screenshot_erro(
                    page=page,
                    codigo_externo="ERRO_CRITICO",
                    identificador_execucao=(
                        identificador_execucao
                    )
                )
            except Exception:
                logger.exception(
                    "Não foi possível salvar o screenshot "
                    "do erro crítico."
                )

    finally:
        fim_execucao = datetime.now()
        tempo_total = fim_execucao - inicio_execucao

        try:
            caminho_relatorio = gerar_relatorio_excel(
                estatisticas=estatisticas,
                identificador_execucao=(
                    identificador_execucao
                ),
                inicio_execucao=inicio_execucao,
                fim_execucao=fim_execucao
            )

            logger.info(
                f"Relatório gerado em: {caminho_relatorio}"
            )

        except Exception:
            caminho_relatorio = None

            logger.exception(
                "Não foi possível gerar o relatório Excel."
            )

        estatisticas.exibir_resumo(tempo_total)

        logger.info(f"Tempo total: {tempo_total}")
        logger.info(f"Log salvo em: {caminho_log}")
        logger.info("Execução finalizada.")

        if caminho_relatorio:
            print(
                f"\nRelatório salvo em: "
                f"{caminho_relatorio}"
            )

        print(f"Log salvo em: {caminho_log}")

        if context:
            context.close()

        if browser:
            browser.close()

        if playwright:
            playwright.stop()

    input(
        "\nPressione ENTER para encerrar..."
    )


if __name__ == "__main__":
    main()