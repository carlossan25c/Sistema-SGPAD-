# domain/excecoes.py
"""
Módulo de exceções personalizadas do SGSA.

Este módulo centraliza todas as exceções de domínio do sistema, ou seja,
erros que representam violações de regras de negócio, transições de estado
inválidas e ações não permitidas dentro do ciclo de vida das solicitações.

Manter as exceções no domínio garante que qualquer camada da aplicação
(rules, application, infrastructure) possa importá-las sem criar
dependências circulares, e que as mensagens de erro sejam sempre
consistentes e descritivas para o usuário final.

Exceções disponíveis:
    - ViolacaoRegraAcademicaError
    - TransicaoEstadoInvalidaError
    - CancelamentoNaoPermitidoError
"""


class ViolacaoRegraAcademicaError(Exception):
    """
    Exceção lançada quando uma regra acadêmica é violada durante a
    validação de uma solicitação (padrão Strategy).

    Esta exceção é o mecanismo central de comunicação de falhas de
    validação no sistema. Em vez de retornar False silenciosamente,
    cada classe de Regra lança esta exceção com uma mensagem clara
    e o nome da regra infringida, facilitando o diagnóstico.

    Atributos:
        regra (str | None): Nome da classe de regra que gerou a exceção,
                            ex: 'RegraPreRequisito'. Útil para logging
                            e para exibição detalhada ao usuário.

    Exemplo de uso:
        >>> raise ViolacaoRegraAcademicaError(
        ...     mensagem="Pré-requisito 'Cálculo 1' não cumprido.",
        ...     regra="RegraPreRequisito"
        ... )

    Exemplo de captura:
        >>> try:
        ...     service.aplicar_regras(solicitacao, regras)
        ... except ViolacaoRegraAcademicaError as e:
        ...     print(e)  # [Violação Acadêmica - RegraPreRequisito] ...
    """

    def __init__(self, mensagem: str, regra: str = None):
        """
        Inicializa a exceção com a mensagem descritiva e o nome da regra.

        :param mensagem: Descrição clara e em linguagem natural do motivo
                         da violação, direcionada ao usuário final.
        :param regra: Nome da classe de regra que originou o erro.
                      Opcional; se omitido, a representação textual não
                      incluirá o nome da regra.
        """
        super().__init__(mensagem)
        self.regra = regra

    def __str__(self) -> str:
        """
        Retorna a representação textual formatada da exceção.

        O formato varia conforme a presença do nome da regra:
          - Com regra:    '[Violação Acadêmica - NomeDaRegra] mensagem'
          - Sem regra:    '[Violação Acadêmica] mensagem'

        :return: String formatada para exibição ao usuário.
        """
        if self.regra:
            return f"[Violação Acadêmica - {self.regra}] {self.args[0]}"
        return f"[Violação Acadêmica] {self.args[0]}"


class TransicaoEstadoInvalidaError(Exception):
    """
    Exceção lançada quando se tenta realizar uma transição de estado
    inválida no ciclo de vida de uma solicitação (padrão State).

    O padrão State define que certas ações só são permitidas em
    determinados estados. Por exemplo, não é possível 'avancar()'
    uma solicitação que já está 'Finalizada', nem 'cancelar()' uma
    que já foi 'Cancelada'. Esta exceção sinaliza que a operação
    solicitada viola o fluxo definido pela máquina de estados.

    Exemplo de uso interno (dentro de EstadoFinalizada):
        >>> raise TransicaoEstadoInvalidaError("Finalizada", "avancar")
        # Resultado: "[Transição Inválida] Ação 'avancar' não permitida
        #             no estado 'Finalizada'."

    Exemplo de captura:
        >>> try:
        ...     solicitacao_aprovada.avancar()
        ... except TransicaoEstadoInvalidaError as e:
        ...     print(e)
    """

    def __init__(self, estado_atual: str, acao: str):
        """
        Inicializa a exceção descrevendo o estado atual e a ação inválida.

        :param estado_atual: Nome do estado em que a solicitação se
                             encontra no momento da tentativa inválida,
                             ex: 'Finalizada', 'Cancelada'.
        :param acao: Nome da ação que foi tentada e não é permitida,
                     ex: 'avancar', 'cancelar', 'rejeitar'.
        """
        mensagem = f"Ação '{acao}' não permitida no estado '{estado_atual}'."
        super().__init__(mensagem)

    def __str__(self) -> str:
        """
        Retorna a representação textual formatada da exceção.

        :return: String no formato '[Transição Inválida] mensagem'.
        """
        return f"[Transição Inválida] {self.args[0]}"


class CancelamentoNaoPermitidoError(Exception):
    """
    Exceção lançada quando o aluno tenta cancelar uma solicitação que
    não está mais no estado 'Aberta'.

    Pela regra de negócio, o aluno só possui autonomia para cancelar
    sua própria solicitação enquanto ela ainda não entrou em análise.
    Uma vez que o setor acadêmico passou a analisá-la (estado 'Em Análise'),
    o cancelamento deve ser solicitado formalmente ao setor responsável.

    Esta exceção comunica essa restrição de forma clara, orientando
    o aluno sobre o próximo passo a tomar.

    Exemplo de captura:
        >>> try:
        ...     solicitacao_em_analise.cancelar()
        ... except CancelamentoNaoPermitidoError as e:
        ...     print(e)
        # [Cancelamento Negado] Cancelamento não permitido: a solicitação
        # está no estado 'Em Análise'. Apenas solicitações 'Aberta' podem...
    """

    def __init__(self, estado_atual: str):
        """
        Inicializa a exceção indicando o estado atual que impede o cancelamento.

        :param estado_atual: Estado em que a solicitação se encontra,
                             ex: 'Em Análise', 'Aprovada', 'Rejeitada'.
        """
        mensagem = (
            f"Cancelamento não permitido: a solicitação está no estado '{estado_atual}'. "
            "Apenas solicitações 'Aberta' podem ser canceladas pelo aluno. "
            "Se já estiver 'Em Análise', solicite o cancelamento ao Setor Acadêmico."
        )
        super().__init__(mensagem)

    def __str__(self) -> str:
        """
        Retorna a representação textual formatada da exceção.

        :return: String no formato '[Cancelamento Negado] mensagem'.
        """
        return f"[Cancelamento Negado] {self.args[0]}"
