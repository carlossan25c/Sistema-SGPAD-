# rules/regra_vinculo_ativo.py
"""
Módulo que implementa a regra de verificação do status do vínculo.

Não faz sentido trancar um curso que já está trancado, assim como um
egresso não possui mais vínculo ativo para trancar. Esta regra impede
essas situações verificando o status do vínculo antes de processar
qualquer trancamento.
"""

from rules.regra_base import Regra
from domain.excecoes import ViolacaoRegraAcademicaError


class RegraVinculoAtivo(Regra):
    """
    Verifica se o aluno possui vínculo 'Ativo' com a instituição.

    Bloqueia a solicitação de trancamento se o status do vínculo for
    'Trancado' (duplo trancamento) ou 'Egresso' (aluno já desligado
    ou formado), pois nenhuma dessas situações permite novo trancamento.

    Aplica-se a: SolicitacaoTrancamento.

    Atributos consultados da solicitação:
        solicitacao.aluno.historico.status_vinculo: situação atual do
            vínculo ('Ativo', 'Trancado' ou 'Egresso').

    Constante de classe:
        VINCULOS_BLOQUEADOS (set): conjunto de status que impedem o
                                   trancamento. {'Trancado', 'Egresso'}.

    Exemplo:
        >>> aluno.historico.status_vinculo = 'Trancado'
        >>> sol = SolicitacaoTrancamento(aluno, disciplina)
        >>> RegraVinculoAtivo().validar(sol)
        # Levanta: "Trancamento não permitido: o aluno possui
        #  vínculo 'Trancado'. Apenas alunos com vínculo 'Ativo'..."
    """

    VINCULOS_BLOQUEADOS: set = {"Trancado", "Egresso"}

    def validar(self, solicitacao) -> bool:
        """
        Verifica se o vínculo do aluno permite o trancamento.

        :param solicitacao: Objeto SolicitacaoTrancamento.
        :raises ViolacaoRegraAcademicaError: se o status do vínculo
                                             for 'Trancado' ou 'Egresso'.
        :return: True se o vínculo for 'Ativo'.
        """
        status = solicitacao.aluno.historico.status_vinculo

        if status in self.VINCULOS_BLOQUEADOS:
            raise ViolacaoRegraAcademicaError(
                mensagem=(
                    f"Trancamento não permitido: o aluno possui vínculo '{status}'. "
                    f"Apenas alunos com vínculo 'Ativo' podem solicitar trancamento."
                ),
                regra="RegraVinculoAtivo"
            )
        return True
