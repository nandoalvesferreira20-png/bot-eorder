class EstatisticasExecucao:
    def __init__(self, total: int):
        self.total = total
        self.canceladas = 0
        self.ja_anuladas = 0
        self.wo_finalizadas = 0
        self.erros = 0
        self.resultados = []

    def registrar(
        self,
        centro_operativo: str,
        codigo_externo: str,
        resultado: str,
        mensagem: str = ""
    ):
        if resultado == "CANCELADA":
            self.canceladas += 1

        elif resultado == "JA_ANULADA":
            self.ja_anuladas += 1

        elif resultado == "WO_FINALIZADA":
            self.wo_finalizadas += 1

        elif resultado == "ERRO":
            self.erros += 1

        self.resultados.append({
            "centro_operativo": centro_operativo,
            "codigo_externo": codigo_externo,
            "resultado": resultado,
            "mensagem": mensagem
        })

    @property
    def processadas(self):
        return len(self.resultados)

    def exibir_resumo(self, tempo_total):
        print("\n" + "=" * 48)
        print("RELATÓRIO FINAL")
        print("=" * 48)
        print(f"Total de TdCs:       {self.total}")
        print(f"Processadas:         {self.processadas}")
        print(f"Canceladas:          {self.canceladas}")
        print(f"Já anuladas:         {self.ja_anuladas}")
        print(f"WO finalizadas:      {self.wo_finalizadas}")
        print(f"Erros:               {self.erros}")
        print(f"Tempo total:         {tempo_total}")
        print("=" * 48)