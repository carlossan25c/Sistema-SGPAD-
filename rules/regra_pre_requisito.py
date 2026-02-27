# rules/regra_pre_requisito.py
"""
Módulo que implementa a regra de verificação de pré-requisitos.

Antes de se matricular em uma disciplina, o aluno deve ter sido aprovado
em todas as disciplinas pré-requisito definidas na grade curricular.
Esta regra consulta o histórico do aluno para verificar cada pré-requisito.
"""

from rules.regra_base import Regra
from domain.excecoes import ViolacaoRegraAcademicaError


class RegraPreRequisito(Regra):
    """
    Valida se o aluno foi aprovado em todos os pré-requisitos da disciplina
    na qual deseja se matricular.

    Para cada disciplina pré-requisito registrada em disciplina.pre_requisitos,
    esta regra consulta historico.foi_aprovado(). Se algum pré-requisito não
    tiver sido cumprido, a regra lança ViolacaoRegraAcademicaError listando
    todos os pendentes de uma vez.

    Aplica-se a: SolicitacaoMatricula.

    Atributos consultados da solicitação:
        solicitacao.disciplina: a disciplina pretendida.
        solicitacao.aluno.historico: para verificar aprovações.

    Exemplo:
        >>> calc2.adicionar_pre_requisito(calc1)
        >>> sol = SolicitacaoMatricula(aluno_sem_calc1, calc2)
        >>> RegraPreRequisito().validar(sol)
        # Levanta: "[Violação Acadêmica - RegraPreRequisito]
        #  Pré-requisito(s) não cumprido(s) para 'Cálculo 2': Cálculo 1."
    """

    def validar(self, solicitacao) -> bool:
        """
        Verifica se todos os pré-requisitos da disciplina foram cumpridos.

        Percorre a lista disciplina.pre_requisitos e consulta o histórico
        do aluno para cada um. Coleta todos os pendentes antes de lançar
        a exceção, para que a mensagem liste todos os problemas de uma vez.

        :param solicitacao: Objeto SolicitacaoMatricula. Se disciplina
                            for None (ex: colação), retorna True
                            imediatamente.
        :raises ViolacaoRegraAcademicaError: com a lista de pré-requisitos
                                             não cumpridos.
        :return: True se todos os pré-requisitos foram satisfeitos.
        """
        disciplina = solicitacao.disciplina
        if disciplina is None:
            return True

        historico = solicitacao.aluno.historico
        pendentes = [
            pre.nome
            for pre in disciplina.pre_requisitos
            if not historico.foi_aprovado(pre)
        ]

        if pendentes:
            raise ViolacaoRegraAcademicaError(
                mensagem=(
                    f"Pré-requisito(s) não cumprido(s) para '{disciplina.nome}': "
                    f"{', '.join(pendentes)}."
                ),
                regra="RegraPreRequisito"
            )
        return True
