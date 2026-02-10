class RelatorioService:
    def gerar_relatorio(self, solicitacoes):
        for s in solicitacoes:
            print(f"Solicitação: {s.__class__.__name__}, Status: {s.status}")
