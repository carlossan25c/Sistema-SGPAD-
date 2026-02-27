# rules/regra_limite_trancamentos.py
"""
Módulo que implementa a regra de limite de trancamentos de curso.

Para evitar o uso abusivo do trancamento como mecanismo de prorrogação
indefinida do curso, a instituição define um número máximo de semestres
que podem ser trancados. Esta regra verifica se o aluno ainda está
dentro desse limite.
"""

from rules.regra_base import Regra
from domain.excecoes import ViolacaoRegraAcademicaError


class RegraLimiteTrancamentos(Regra):
    """
    Verifica se o aluno ainda possui trancamentos disponíveis.

    Consulta historico.trancamentos (contador de trancamentos já realizados)
    e compara com o limite configurado. O limite padrão é 4 semestres,
    mas pode ser personalizado por instância.

    Aplica-se a: SolicitacaoTrancamento.

    Configuração:
        O limite pode ser ajustado ao instanciar a regra:
        >>> regra = RegraLimiteTrancamentos(limite=2)  # máx. 2 trancamentos

    Constante de classe:
        LIMITE_PADRAO (int): valor padrão de 4 trancamentos.

    Atributos consultados da solicitação:
        solicitacao.aluno.historico.trancamentos: número de trancamentos
            já realizados pelo aluno.

    Exemplo:
        >>> aluno.historico._trancamentos = 4
        >>> sol = SolicitacaoTrancamento(aluno, disciplina)
        >>> RegraLimiteTrancamentos().validar(sol)
        # Levanta: "Limite de trancamentos atingido.
        #  O aluno já realizou 4 trancamento(s) (máximo: 4)."
    """

    LIMITE_PADRAO: int = 4

    def __init__(self, limite: int = None):
        """
        Inicializa a regra com o limite de trancamentos desejado.

        :param limite: Número máximo de trancamentos permitidos.
                       Se None, usa LIMITE_PADRAO (4).
        """
        self._limite = limite if limite is not None else self.LIMITE_PADRAO

    def validar(self, solicitacao) -> bool:
        """
        Verifica se o aluno não atingiu o limite de trancamentos.

        :param solicitacao: Objeto SolicitacaoTrancamento.
        :raises ViolacaoRegraAcademicaError: se trancamentos >= limite,
                                             com o número atual e o limite.
        :return: True se o aluno ainda possui trancamentos disponíveis.
        """
        trancamentos_realizados = solicitacao.aluno.historico.trancamentos

        if trancamentos_realizados >= self._limite:
            raise ViolacaoRegraAcademicaError(
                mensagem=(
                    f"Limite de trancamentos atingido. "
                    f"O aluno já realizou {trancamentos_realizados} trancamento(s) "
                    f"(máximo permitido: {self._limite})."
                ),
                regra="RegraLimiteTrancamentos"
            )
        return True
