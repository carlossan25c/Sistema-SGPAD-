# domain/solicitacao_trancamento.py
"""
Módulo que representa o pedido de trancamento de uma disciplina.

O trancamento é a interrupção temporária da matrícula em uma disciplina
específica. Para ser válido, deve respeitar o prazo do calendário acadêmico,
o limite de trancamentos do aluno e seu status de vínculo ativo.
"""

import datetime
from domain.solicitacao import Solicitacao


class SolicitacaoTrancamento(Solicitacao):
    """
    Pedido formal de interrupção temporária da matrícula em uma disciplina.

    Especializa Solicitacao adicionando os atributos de data e prazo,
    necessários para a validação pela RegraPrazo. A data representa
    quando a solicitação foi feita; o prazo é o último dia permitido
    pelo calendário acadêmico para esse tipo de pedido.

    Herança:
        Solicitacao → SolicitacaoTrancamento.

    Regras de validação aplicáveis (Strategy):
        - RegraPrazo: garante que a solicitação está dentro do período
                      permitido pelo calendário acadêmico.
        - RegraLimiteTrancamentos: verifica se o aluno ainda possui
                                   trancamentos disponíveis (máx. 4).
        - RegraVinculoAtivo: impede trancamento se o vínculo já for
                             'Trancado' ou 'Egresso'.

    Atributos extras:
        data (datetime.date): Data em que a solicitação foi realizada.
                              Padrão: hoje.
        prazo (datetime.date): Último dia permitido para trancamento
                               conforme o calendário acadêmico.
                               Padrão: hoje (sem prazo restritivo).

    Exemplo de uso:
        >>> prazo_semestre = datetime.date(2025, 10, 31)
        >>> sol = SolicitacaoTrancamento(aluno, disciplina_poo,
        ...     data=datetime.date.today(),
        ...     prazo=prazo_semestre)
        >>> service.aplicar_regras(sol, regras_trancamento)
    """

    def __init__(self, aluno, disciplina,
                 data: datetime.date = None,
                 prazo: datetime.date = None):
        """
        Inicializa o pedido de trancamento com disciplina e datas.

        :param aluno: Objeto Aluno que deseja trancar a disciplina.
        :param disciplina: Objeto Disciplina a ser trancada.
        :param data: Data de realização da solicitação. Se None,
                     usa datetime.date.today().
        :param prazo: Prazo limite definido pelo calendário acadêmico.
                      Se None, usa datetime.date.today() (sem restrição).
                      Para aplicar restrição real, deve ser informado.
        """
        super().__init__(aluno, disciplina=disciplina)
        self.data = data or datetime.date.today()
        self.prazo = prazo or datetime.date.today()
