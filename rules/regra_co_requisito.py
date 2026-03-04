# rules/regra_co_requisito.py
"""
Módulo que implementa a regra de co-requisitos de matrícula.

Certas disciplinas exigem matrícula simultânea em outras (ex: Teoria de Física
e seu Laboratório). Esta regra garante que o aluno está matriculando ambas
juntas, ou que já foi aprovado na co-requisitada anteriormente.
"""

from rules.regra_base import Regra
from domain.excecoes import ViolacaoRegraAcademicaError


class RegraCoRequisito(Regra):
    """
    Valida se os co-requisitos da disciplina estão sendo cursados
    simultaneamente ou já foram concluídos com aprovação.

    Um co-requisito pode ser satisfeito de duas formas:
      1. O aluno já foi aprovado na disciplina co-requisito (histórico), OU
      2. A disciplina co-requisito está em
         solicitacao.disciplinas_co_req_solicitadas, indicando que o aluno
         está se matriculando em ambas no mesmo momento.

    Aplica-se a: SolicitacaoMatricula.

    Atributos consultados da solicitação:
        solicitacao.disciplina: a disciplina pretendida.
        solicitacao.aluno.historico: para verificar aprovações anteriores.
        solicitacao.disciplinas_co_req_solicitadas: lista de disciplinas
            sendo matriculadas simultaneamente neste pedido.

    Exemplo:
        >>> teoria.adicionar_co_requisito(lab)
        >>> # Aluno sem lab no histórico e sem lab nas simultâneas:
        >>> sol = SolicitacaoMatricula(aluno, teoria)
        >>> RegraCoRequisito().validar(sol)
        # Levanta: "Co-requisito(s) não atendido(s) para 'Teoria': Laboratório..."
        >>>
        >>> # Aluno incluindo lab nas simultâneas:
        >>> sol2 = SolicitacaoMatricula(aluno, teoria,
        ...     disciplinas_co_req_solicitadas=[lab])
        >>> RegraCoRequisito().validar(sol2)
        True
    """

    def validar(self, solicitacao) -> bool:
        """
        Verifica se todos os co-requisitos estão sendo atendidos.

        Para cada co-requisito da disciplina, verifica se o aluno já foi
        aprovado anteriormente ou se está matriculando-se simultaneamente.
        Lista todos os co-requisitos pendentes antes de lançar a exceção.

        :param solicitacao: Objeto SolicitacaoMatricula. Se disciplina
                            for None, retorna True imediatamente.
        :raises ViolacaoRegraAcademicaError: com a lista de co-requisitos
                                             não atendidos.
        :return: True se todos os co-requisitos estão satisfeitos.
        """
        disciplina = solicitacao.disciplina
        if disciplina is None:
            return True

        historico = solicitacao.aluno.historico
        simultaneas = getattr(solicitacao, "disciplinas_co_req_solicitadas", [])

        pendentes = []
        for co in disciplina.co_requisitos:
            ja_aprovado = historico.foi_aprovado(co)
            sendo_matriculado = co in simultaneas
            if not ja_aprovado and not sendo_matriculado:
                pendentes.append(co.nome)

        if pendentes:
            raise ViolacaoRegraAcademicaError(
                mensagem=(
                    f"Co-requisito(s) não atendido(s) para '{disciplina.nome}': "
                    f"{', '.join(pendentes)}. "
                    f"Matricule-se nessas disciplinas simultaneamente."
                ),
                regra="RegraCoRequisito"
            )
        return True
