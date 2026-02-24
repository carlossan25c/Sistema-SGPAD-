class RelatorioService:
    """
    Serviço para geração de logs e visões consolidadas de dados.
    """
    def gerar_relatorio(self, solicitacoes):
        """
        Itera sobre uma lista de solicitações e exibe o resumo em tela.
        :param solicitacoes: Lista de objetos da classe Solicitacao.
        """
        for s in solicitacoes:
            print(f"Solicitação: {s.__class__.__name__}, Status: {s.status}")
