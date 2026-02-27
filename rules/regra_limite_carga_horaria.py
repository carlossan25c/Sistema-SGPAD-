# rules/regra_limite_carga_horaria.py
"""
Módulo que implementa a regra de limite de carga horária semestral.

Cada curso define um teto de horas que um aluno pode cursar em um único
semestre. Esta regra soma a carga horária já matriculada com a da nova
disciplina e verifica se o total não ultrapassa o limite do curso.
"""

from rules.regra_base import Regra
from domain.excecoes import ViolacaoRegraAcademicaError


class RegraLimiteCargaHoraria(Regra):
    """
    Valida se a carga horária total do semestre, após a nova matrícula,
    não excede o limite máximo definido pelo curso.

    O limite é consultado diretamente em aluno.curso.limite_horas_semestrais,
    tornando a regra configurável por curso sem necessidade de alteração
    no código (OCP).

    Aplica-se a: SolicitacaoMatricula.

    Atributos consultados da solicitação:
        solicitacao.disciplina: carga horária da nova disciplina.
        solicitacao.aluno.curso.limite_horas_semestrais: teto do curso.
        solicitacao.carga_horaria_semestre_atual: horas já matriculadas
            no semestre corrente. Deve ser definido externamente antes
            de aplicar a regra. Se ausente, assume 0.

    Exemplo:
        >>> curso = Curso("Eng. Software", limite_horas_semestrais=360)
        >>> sol = SolicitacaoMatricula(aluno, disciplina_de_200h)
        >>> sol.carga_horaria_semestre_atual = 200
        >>> RegraLimiteCargaHoraria().validar(sol)
        # Levanta: "Limite de carga horária semestral excedido.
        #  Limite: 360h, atual: 200h, solicitada: 200h (total: 400h)."
    """

    def validar(self, solicitacao) -> bool:
        """
        Verifica se adicionar a nova disciplina não excede o teto semestral.

        Calcula o total que o aluno teria após a matrícula (horas atuais +
        horas da nova disciplina) e compara com o limite do curso.

        :param solicitacao: Objeto SolicitacaoMatricula. Se disciplina
                            for None, retorna True imediatamente.
        :raises ViolacaoRegraAcademicaError: se o total resultante
                                             ultrapassar o limite do curso,
                                             com detalhamento dos valores.
        :return: True se a carga total respeitar o limite.
        """
        disciplina = solicitacao.disciplina
        if disciplina is None:
            return True

        limite = solicitacao.aluno.curso.limite_horas_semestrais
        ja_matriculado = getattr(solicitacao, "carga_horaria_semestre_atual", 0)
        nova_carga = ja_matriculado + disciplina.carga_horaria

        if nova_carga > limite:
            raise ViolacaoRegraAcademicaError(
                mensagem=(
                    f"Limite de carga horária semestral excedido. "
                    f"Limite do curso: {limite}h, "
                    f"carga atual: {ja_matriculado}h, "
                    f"disciplina solicitada: {disciplina.carga_horaria}h "
                    f"(total seria {nova_carga}h)."
                ),
                regra="RegraLimiteCargaHoraria"
            )
        return True
