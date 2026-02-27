# rules/regra_elegibilidade.py
"""
Módulo que implementa a regra de elegibilidade para colação de grau.

Para colar grau, o aluno deve ter integralizado 100% das disciplinas
obrigatórias do curso e cumprido o mínimo de horas em disciplinas
optativas ou de atividades complementares. Esta regra verifica ambas
as condições.
"""

from rules.regra_base import Regra
from domain.excecoes import ViolacaoRegraAcademicaError


class RegraElegibilidade(Regra):
    """
    Verifica se o aluno integralizou o currículo para colar grau.

    Realiza duas verificações em sequência:
      1. Integralização obrigatória: todas as disciplinas marcadas com
         obrigatoria=True no curso devem constar em historico com nota
         >= NOTA_MINIMA_APROVACAO.
      2. Mínimo de optativas: a soma da carga horária das disciplinas
         optativas aprovadas (obrigatoria=False) deve atingir
         curso.min_horas_optativas. Esta verificação só ocorre se
         min_horas_optativas > 0.

    Aplica-se a: SolicitacaoColacao.

    Atributos consultados da solicitação:
        solicitacao.aluno.curso: para obter obrigatórias e min_horas_optativas.
        solicitacao.aluno.historico: para verificar aprovações e calcular
            horas de optativas concluídas.

    Exemplo:
        >>> curso = Curso("ADS", min_horas_optativas=120)
        >>> tcc = Disciplina("TCC", 80, obrigatoria=True)
        >>> curso.adicionar_disciplina(tcc)
        >>> sol = SolicitacaoColacao(aluno_sem_tcc, curso)
        >>> RegraElegibilidade().validar(sol)
        # Levanta: "Integralização curricular incompleta.
        #  Disciplina(s) obrigatória(s) pendente(s): TCC."
    """

    def validar(self, solicitacao) -> bool:
        """
        Verifica integralização das obrigatórias e mínimo de optativas.

        As duas verificações são realizadas separadamente: se as obrigatórias
        não estiverem completas, a exceção é lançada imediatamente, sem
        verificar optativas. Isso dá prioridade ao erro mais grave.

        :param solicitacao: Objeto SolicitacaoColacao.
        :raises ViolacaoRegraAcademicaError: se houver obrigatórias pendentes
                                             ou carga de optativas insuficiente.
        :return: True se o aluno está apto a colar grau.
        """
        aluno = solicitacao.aluno
        historico = aluno.historico
        curso = aluno.curso

        # --- 1. Verificação das disciplinas obrigatórias ---
        obrigatorias = curso.disciplinas_obrigatorias()
        nao_integralizadas = [
            d.nome for d in obrigatorias if not historico.foi_aprovado(d)
        ]
        if nao_integralizadas:
            raise ViolacaoRegraAcademicaError(
                mensagem=(
                    f"Integralização curricular incompleta. "
                    f"Disciplina(s) obrigatória(s) pendente(s): "
                    f"{', '.join(nao_integralizadas)}."
                ),
                regra="RegraElegibilidade"
            )

        # --- 2. Verificação do mínimo de optativas ---
        min_optativas = curso.min_horas_optativas
        if min_optativas > 0:
            horas_optativas = sum(
                d.carga_horaria
                for d in historico.disciplinas_aprovadas()
                if not d.obrigatoria
            )
            if horas_optativas < min_optativas:
                raise ViolacaoRegraAcademicaError(
                    mensagem=(
                        f"Carga horária de optativas insuficiente. "
                        f"Mínimo exigido pelo curso: {min_optativas}h, "
                        f"concluído pelo aluno: {horas_optativas}h."
                    ),
                    regra="RegraElegibilidade"
                )

        return True
