# rules/regra_elegibilidade.py
"""
Módulo que implementa a regra de elegibilidade para colação de grau.
"""

from rules.regra_base import Regra
from domain.excecoes import ViolacaoRegraAcademicaError

MINIMO_CREDITOS_FALLBACK = 120  # usado quando o curso não tem disciplinas cadastradas


class RegraElegibilidade(Regra):
    """
    Verifica se o aluno integralizou o currículo para colar grau.

    Realiza até três verificações em sequência:
      1. Se o curso tiver disciplinas obrigatórias cadastradas, verifica
         se o aluno foi aprovado em todas elas.
      2. Se o curso exigir mínimo de optativas, verifica o total de horas.
      3. Se o curso não tiver disciplinas cadastradas (fallback), exige
         pelo menos MINIMO_CREDITOS_FALLBACK horas aprovadas no histórico —
         garantindo que a regra nunca passe automaticamente para um aluno
         sem histórico.

    Aplica-se a: SolicitacaoColacao.
    """

    def validar(self, solicitacao) -> bool:
        aluno = solicitacao.aluno
        historico = aluno.historico
        curso = aluno.curso

        obrigatorias = curso.disciplinas_obrigatorias()

        # --- Fallback: curso sem disciplinas cadastradas ---
        if not obrigatorias:
            total = historico.total_creditos()
            if total < MINIMO_CREDITOS_FALLBACK:
                raise ViolacaoRegraAcademicaError(
                    mensagem=(
                        f"Integralização curricular não verificável: o curso '{curso.nome}' "
                        f"não possui disciplinas cadastradas no sistema. "
                        f"Para garantir a elegibilidade, o aluno deve ter ao menos "
                        f"{MINIMO_CREDITOS_FALLBACK}h de créditos aprovados no histórico. "
                        f"Total atual: {total}h."
                    ),
                    regra="RegraElegibilidade"
                )
            return True

        # --- 1. Verificação das disciplinas obrigatórias ---
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
