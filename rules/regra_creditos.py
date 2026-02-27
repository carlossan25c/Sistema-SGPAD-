# rules/regra_creditos.py
"""
Módulo que implementa a regra geral de créditos mínimos.

Algumas solicitações exigem que o aluno já tenha acumulado um número
mínimo de horas no histórico antes de poderem ser realizadas. Esta
regra oferece uma verificação genérica e configurável de créditos.
"""

from rules.regra_base import Regra
from domain.excecoes import ViolacaoRegraAcademicaError


class RegraCreditos(Regra):
    """
    Valida se o aluno possui ao menos o mínimo de créditos (horas)
    aprovados no histórico.

    Esta é uma regra genérica e reutilizável: o mínimo exigido é
    configurado ao instanciar a regra. Pode ser usada em conjunto
    com outras regras para qualquer tipo de solicitação que exija
    um patamar mínimo de progresso acadêmico.

    Atributos consultados da solicitação:
        solicitacao.aluno.historico.total_creditos(): soma das cargas
            horárias de todas as disciplinas aprovadas.

    Configuração:
        >>> regra = RegraCreditos(minimo=120)  # exige ao menos 120h aprovadas

    Exemplo:
        >>> aluno.historico.adicionar_disciplina(disc_60h, nota=4.0)  # reprovado
        >>> sol = SolicitacaoMatricula(aluno, disciplina)
        >>> RegraCreditos(minimo=80).validar(sol)
        # Levanta: "Créditos insuficientes.
        #  Mínimo exigido: 80h, total do aluno: 0h."
    """

    def __init__(self, minimo: int = 80):
        """
        Inicializa a regra com o mínimo de créditos exigido.

        :param minimo: Total mínimo de horas-crédito aprovadas que o aluno
                       deve possuir. Padrão: 80h.
        """
        self._minimo = minimo

    def validar(self, solicitacao) -> bool:
        """
        Verifica se o aluno atingiu o mínimo de créditos exigido.

        :param solicitacao: Qualquer objeto Solicitacao — esta regra
                            não é restrita a um tipo específico.
        :raises ViolacaoRegraAcademicaError: se total_creditos() <
                                             mínimo configurado.
        :return: True se o aluno possui créditos suficientes.
        """
        total = solicitacao.aluno.historico.total_creditos()

        if total < self._minimo:
            raise ViolacaoRegraAcademicaError(
                mensagem=(
                    f"Créditos insuficientes. "
                    f"Mínimo exigido: {self._minimo}h, "
                    f"total do aluno: {total}h."
                ),
                regra="RegraCreditos"
            )
        return True
