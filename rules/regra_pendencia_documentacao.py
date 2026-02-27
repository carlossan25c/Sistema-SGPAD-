# rules/regra_pendencia_documentacao.py
"""
Módulo que implementa a regra de verificação de pendências documentais.

Pendências como débitos na biblioteca ou documentos de registro civil
incompletos impedem a emissão do diploma e, portanto, bloqueiam a
solicitação de colação de grau antes mesmo de chegar ao setor acadêmico.
"""

from rules.regra_base import Regra
from domain.excecoes import ViolacaoRegraAcademicaError


class RegraPendenciaDocumentacao(Regra):
    """
    Verifica se o aluno possui pendências abertas que impeçam a colação.

    Consulta aluno.tem_pendencias() e, se True, lista todas as pendências
    registradas na mensagem de erro, orientando o aluno a regularizá-las
    antes de prosseguir.

    Aplica-se a: SolicitacaoColacao.

    Tipos comuns de pendências:
        - Débito na biblioteca (livros não devolvidos ou multas).
        - Certidão de nascimento ou CPF pendente no registro.
        - Documentação de colação anterior incompleta.

    Atributos consultados da solicitação:
        solicitacao.aluno.tem_pendencias(): boolean indicador.
        solicitacao.aluno.pendencias: lista de strings descritivas.

    Exemplo:
        >>> aluno.adicionar_pendencia("Débito na biblioteca")
        >>> aluno.adicionar_pendencia("Certidão de nascimento pendente")
        >>> sol = SolicitacaoColacao(aluno, curso)
        >>> RegraPendenciaDocumentacao().validar(sol)
        # Levanta: "Colação de grau negada: o aluno possui pendência(s)
        #  não resolvida(s): Débito na biblioteca,
        #  Certidão de nascimento pendente. Regularize antes..."
    """

    def validar(self, solicitacao) -> bool:
        """
        Verifica se o aluno está livre de pendências documentais.

        :param solicitacao: Objeto SolicitacaoColacao.
        :raises ViolacaoRegraAcademicaError: se o aluno possuir qualquer
                                             pendência registrada, listando
                                             todas na mensagem de erro.
        :return: True se o aluno não possuir pendências.
        """
        aluno = solicitacao.aluno

        if aluno.tem_pendencias():
            pendencias = ", ".join(aluno.pendencias)
            raise ViolacaoRegraAcademicaError(
                mensagem=(
                    f"Colação de grau negada: o aluno possui pendência(s) "
                    f"não resolvida(s): {pendencias}. "
                    f"Regularize-as antes de solicitar a formatura."
                ),
                regra="RegraPendenciaDocumentacao"
            )
        return True
