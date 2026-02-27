# domain/solicitacao_colacao.py
"""
Módulo que representa o pedido de colação de grau (formatura).

A colação de grau é a solicitação mais exigente do sistema: requer que
o aluno tenha integralizado 100% das disciplinas obrigatórias, cumprido
o mínimo de optativas e não possua nenhuma pendência documental ou
de biblioteca em aberto.
"""

from domain.solicitacao import Solicitacao


class SolicitacaoColacao(Solicitacao):
    """
    Pedido formal de colação de grau (formatura) realizado pelo aluno.

    Esta solicitação é vinculada ao Curso do aluno (não a uma disciplina
    específica) e está sujeita às regras de integralização curricular
    e de pendências documentais.

    Herança:
        Solicitacao → SolicitacaoColacao.

    Regras de validação aplicáveis (Strategy):
        - RegraElegibilidade: verifica se o aluno concluiu todas as
                              disciplinas obrigatórias e o mínimo de
                              optativas/atividades complementares
                              exigido pelo curso.
        - RegraPendenciaDocumentacao: nega a solicitação se houver
                                      débitos na biblioteca ou
                                      documentos de registro civil
                                      pendentes.

    Atributo herdado relevante:
        curso: Objeto Curso no qual o aluno deseja colar grau.
               Fornecido via super().__init__() com curso=curso.

    Exemplo de uso:
        >>> sol = SolicitacaoColacao(aluno, aluno.curso)
        >>> service.aplicar_regras(sol, [
        ...     RegraElegibilidade(),
        ...     RegraPendenciaDocumentacao()
        ... ])
    """

    def __init__(self, aluno, curso):
        """
        Inicializa o pedido de colação de grau vinculado ao curso.

        :param aluno: Objeto Aluno que deseja colar grau.
                      Deve ter integralizado o currículo e não ter
                      pendências — verificado pelas regras de validação.
        :param curso: Objeto Curso no qual o aluno pretende graduar-se.
                      Em geral, deve ser o mesmo curso ao qual o aluno
                      está vinculado (aluno.curso).
        """
        super().__init__(aluno, curso=curso)
