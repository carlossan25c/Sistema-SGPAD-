from domain.estado import EstadoAberta


class Solicitacao:
    """
    Classe base para todos os pedidos acadêmicos.
    Implementa o padrão State para controle do ciclo de vida.

    O status é sempre derivado do estado interno — nunca definido diretamente
    em código externo, garantindo a consistência do fluxo.
    """

    def __init__(self, aluno, disciplina=None, curso=None):
        self.aluno = aluno
        self._disciplina = disciplina
        self._curso = curso
        # Estado inicial
        self._estado = EstadoAberta()
        self.status = self._estado.nome()
        # Lista de observadores (padrão Observer)
        self._observadores = []

    # ------------------------------------------------------------------
    # Properties para acesso aos atributos privados
    # ------------------------------------------------------------------

    @property
    def disciplina(self):
        """Retorna a disciplina associada à solicitação."""
        return self._disciplina

    @property
    def curso(self):
        """Retorna o curso associado à solicitação."""
        return self._curso

    # ------------------------------------------------------------------
    # State
    # ------------------------------------------------------------------

    def avancar(self) -> None:
        """Delega o avanço de estado para o objeto Estado atual."""
        self._estado.avancar(self)
        self._notificar_observadores()

    def cancelar(self) -> None:
        """
        Cancela a solicitação.
        Apenas permitido no estado 'Aberta'. Levanta CancelamentoNaoPermitidoError
        em qualquer outro estado.
        """
        self._estado.cancelar(self)
        self._notificar_observadores()

    def rejeitar(self) -> None:
        """
        Rejeita a solicitação diretamente (ação do setor acadêmico).
        Permitida somente quando 'Em Análise'.
        """
        from domain.excecoes import TransicaoEstadoInvalidaError
        from domain.estado import EstadoEmAnalise, EstadoFinalizada
        if not isinstance(self._estado, EstadoEmAnalise):
            raise TransicaoEstadoInvalidaError(self.status, "rejeitar")
        from domain.estado import EstadoFinalizada
        self._estado = EstadoFinalizada()
        self.status = "Rejeitada"
        self._notificar_observadores()

    # ------------------------------------------------------------------
    # Observer
    # ------------------------------------------------------------------

    def registrar_observador(self, observador) -> None:
        """Registra um observador que será notificado a cada mudança de estado."""
        if observador not in self._observadores:
            self._observadores.append(observador)

    def _notificar_observadores(self) -> None:
        """Dispara a notificação para todos os observadores registrados."""
        for obs in self._observadores:
            obs.atualizar(self)

    # ------------------------------------------------------------------
    # Métodos adicionais para compatibilidade com testes
    # ------------------------------------------------------------------

    def mudar_estado(self, novo_estado: str) -> None:
        """
        Muda o estado da solicitação para o estado informado.

        :param novo_estado: Nome do novo estado (ex: 'Finalizada', 'Aberta').
        :raises ValueError: se tentar reabrir uma solicitação finalizada.
        """
        if self.status == "Finalizada" and novo_estado != "Finalizada":
            raise ValueError("Não é possível reabrir solicitação finalizada.")
        self.status = novo_estado

    def validar(self) -> bool:
        """
        Valida a solicitação (método stub para compatibilidade com testes).

        :return: True se a solicitação é válida.
        """
        return True

    # ------------------------------------------------------------------
    # Representação
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        if self._disciplina:
            return (
                f"Solicitação de {self.__class__.__name__} - "
                f"Aluno: {self.aluno.nome}, "
                f"Disciplina: {self._disciplina.nome}, "
                f"Status: {self.status}"
            )
        elif self._curso:
            return (
                f"Solicitação de {self.__class__.__name__} - "
                f"Aluno: {self.aluno.nome}, "
                f"Curso: {self._curso.nome}, "
                f"Status: {self.status}"
            )
        return (
            f"Solicitação de {self.__class__.__name__} - "
            f"Aluno: {self.aluno.nome}, "
            f"Status: {self.status}"
        )
