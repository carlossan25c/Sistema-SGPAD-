# application/relatorio_service.py
"""
Módulo que implementa o serviço de geração de relatórios do SGSA.

Fornece uma visão consolidada das solicitações registradas no sistema,
útil para auditoria, acompanhamento administrativo e geração de logs.
"""


class RelatorioService:
    """
    Serviço responsável pela geração de relatórios e logs de solicitações.

    Atualmente gera relatórios em formato de texto no console, mas pode
    ser estendido para exportar em PDF, CSV ou HTML sem alterar o código
    que o utiliza (OCP).

    Princípios SOLID:
        - SRP: responsabilidade única de formatar e exibir relatórios.
        - OCP: novos formatos de saída podem ser adicionados por
               extensão desta classe (subclasses ou parâmetros).

    Exemplo de uso:
        >>> relatorio = RelatorioService()
        >>> relatorio.gerar_relatorio([sol1, sol2, sol3])
        # ============================================================
        #   RELATÓRIO DE SOLICITAÇÕES
        # ============================================================
        #   01. [SolicitacaoMatricula] Aluno: João | Status: Aberta
        #   02. [SolicitacaoTrancamento] Aluno: Maria | Status: Aprovada
        # ============================================================
    """

    def gerar_relatorio(self, solicitacoes: list) -> None:
        """
        Exibe no console um relatório formatado com o resumo de todas
        as solicitações recebidas.

        Itera sobre a lista e imprime uma linha por solicitação com:
        número sequencial, tipo da solicitação, nome do aluno e status.

        :param solicitacoes: Lista de objetos Solicitacao (ou subclasses)
                             a serem incluídos no relatório. Pode ser
                             vazia — nesse caso, o relatório é exibido
                             sem itens.
        """
        print("\n" + "=" * 60)
        print("  RELATÓRIO DE SOLICITAÇÕES")
        print("=" * 60)

        if not solicitacoes:
            print("  Nenhuma solicitação registrada.")
        else:
            for i, s in enumerate(solicitacoes, start=1):
                print(
                    f"  {i:02d}. [{s.__class__.__name__}] "
                    f"Aluno: {s.aluno.nome} | Status: {s.status}"
                )

        print("=" * 60 + "\n")
