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
    """

    def validar(self, solicitacao) -> bool:
        aluno = solicitacao.aluno
        historico = aluno.historico
        curso = aluno.curso

        obrigatorias = curso.disciplinas_obrigatorias()
        min_optativas = curso.min_horas_optativas

    
        if not obrigatorias and min_optativas == 0:
            total = historico.total_creditos()
            if total < MINIMO_CREDITOS_FALLBACK:
                raise ViolacaoRegraAcademicaError(
                    mensagem=(
                        f"Integralização não verificável: o curso '{curso.nome}' "
                        f"está vazio no sistema. Exigido ao menos {MINIMO_CREDITOS_FALLBACK}h. "
                        f"Total atual: {total}h."
                    ),
                    regra="RegraElegibilidade"
                )
            return True # Curso vazio, mas aluno tem horas suficientes.

        # --- 1. Verificação das disciplinas obrigatórias ---
        # Se houver obrigatórias, elas DEVEM ser checadas primeiro.
        if obrigatorias:
            nao_integralizadas = [
                d.nome for d in obrigatorias if not historico.foi_aprovado(d)
            ]
            if nao_integralizadas:
                raise ViolacaoRegraAcademicaError(
                    mensagem=(
                        f"Integralização incompleta. Disciplina(s) "
                        f"obrigatória(s) pendente(s): {', '.join(nao_integralizadas)}."
                    ),
                    regra="RegraElegibilidade"
                )

        # --- 2. Verificação do mínimo de optativas ---
        # Se o curso exige optativas, checamos agora, mesmo que não tenha obrigatórias.
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
                        f"Mínimo exigido: {min_optativas}h, "
                        f"concluído: {horas_optativas}h."
                    ),
                    regra="RegraElegibilidade"
                )

        # Se passou por todas as travas acima, o aluno está apto.
        return True