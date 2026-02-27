# domain/solicitacao_matricula.py
"""
Módulo que representa o pedido de matrícula em uma disciplina.

A SolicitacaoMatricula é o subtipo de solicitação mais comum do sistema.
Ela carrega, além dos dados básicos, a lista de disciplinas sendo
matriculadas simultaneamente — necessária para validar co-requisitos.
"""

from domain.solicitacao import Solicitacao


class SolicitacaoMatricula(Solicitacao):
    """
    Pedido formal de inclusão de um aluno em uma nova disciplina.

    Especializa Solicitacao adicionando suporte a co-requisitos simultâneos.
    Quando uma disciplina exige matrícula simultânea em outra (co-requisito),
    o aluno deve informar todas as disciplinas que está matriculando juntas
    através do atributo disciplinas_co_req_solicitadas.

    Herança:
        Solicitacao → SolicitacaoMatricula.

    Regras de validação aplicáveis (Strategy):
        - RegraPreRequisito: verifica aprovação prévia nos pré-requisitos.
        - RegraCoRequisito: verifica matrícula simultânea nos co-requisitos.
        - RegraLimiteCargaHoraria: verifica respeito ao teto semestral.

    Notificação automática (Observer):
        - Ao ser criada via SolicitacaoService, a Coordenação do Curso
          é notificada automaticamente.

    Atributo extra:
        disciplinas_co_req_solicitadas (list[Disciplina]): disciplinas
            que o aluno está matriculando no mesmo ato, utilizadas pela
            RegraCoRequisito para verificar co-requisitos.

    Atributo opcional da solicitação (definido externamente):
        carga_horaria_semestre_atual (int): total de horas já matriculadas
            no semestre corrente, necessário para RegraLimiteCargaHoraria.
            Deve ser definido antes de aplicar as regras.

    Exemplo de uso:
        >>> sol = SolicitacaoMatricula(aluno, calc2,
        ...     disciplinas_co_req_solicitadas=[lab_calc])
        >>> sol.carga_horaria_semestre_atual = 180
        >>> service.aplicar_regras(sol, regras_matricula)
    """

    def __init__(self, aluno, disciplina,
                 disciplinas_co_req_solicitadas=None):
        """
        Inicializa o pedido de matrícula com a disciplina desejada.

        :param aluno: Objeto Aluno que deseja se matricular.
        :param disciplina: Objeto Disciplina na qual o aluno quer
                           se matricular.
        :param disciplinas_co_req_solicitadas: Lista opcional de objetos
                           Disciplina que estão sendo matriculadas
                           simultaneamente para satisfazer co-requisitos.
                           Se None, assume lista vazia.
        """
        super().__init__(aluno, disciplina=disciplina)
        self.disciplinas_co_req_solicitadas = disciplinas_co_req_solicitadas or []
