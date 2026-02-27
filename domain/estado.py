# domain/estado.py
"""
Módulo que implementa o padrão de projeto State para o ciclo de vida
das solicitações acadêmicas.

O padrão State permite que um objeto (Solicitacao) altere seu comportamento
quando seu estado interno muda, encapsulando cada estado em uma classe
separada. Isso elimina longas cadeias de if/elif sobre o status e garante
que transições inválidas sejam detectadas e bloqueadas automaticamente.

Fluxo de estados permitido:
    Aberta → Em Análise → Finalizada (Aprovada ou Rejeitada)
    Aberta → Cancelada

Transições proibidas (levantam TransicaoEstadoInvalidaError):
    - Qualquer ação sobre um estado terminal (Finalizada ou Cancelada).
    - Cancelamento pelo aluno em 'Em Análise' (levanta CancelamentoNaoPermitidoError).

Classes disponíveis:
    EstadoSolicitacao (ABC) — interface base
    EstadoAberta
    EstadoEmAnalise
    EstadoFinalizada
    EstadoCancelada
"""

from abc import ABC, abstractmethod
from domain.excecoes import TransicaoEstadoInvalidaError, CancelamentoNaoPermitidoError


class EstadoSolicitacao(ABC):
    """
    Interface base (abstrata) para todos os estados do ciclo de vida
    de uma solicitação acadêmica.

    Define o contrato que cada estado concreto deve implementar:
    - avancar(): leva a solicitação para o próximo estado.
    - cancelar(): cancela a solicitação (quando permitido).
    - nome(): retorna o nome textual do estado.

    Padrão aplicado: State (GoF).

    Princípios SOLID:
        - OCP: novos estados podem ser adicionados sem modificar os existentes.
        - LSP: todos os estados concretos respeitam este contrato.
        - DIP: Solicitacao depende desta abstração, não das implementações.
    """

    @abstractmethod
    def avancar(self, solicitacao) -> None:
        """
        Avança a solicitação para o próximo estado no fluxo definido.

        :param solicitacao: Objeto Solicitacao cujo estado será alterado.
        :raises TransicaoEstadoInvalidaError: se a transição não for
                                              permitida neste estado.
        """

    @abstractmethod
    def cancelar(self, solicitacao) -> None:
        """
        Cancela a solicitação, se a ação for permitida neste estado.

        :param solicitacao: Objeto Solicitacao a ser cancelado.
        :raises CancelamentoNaoPermitidoError: se o estado não permitir
                                               cancelamento pelo aluno.
        :raises TransicaoEstadoInvalidaError: se o estado for terminal.
        """

    @abstractmethod
    def nome(self) -> str:
        """
        Retorna o nome textual deste estado.

        :return: String identificando o estado (ex: 'Aberta', 'Em Análise').
        """


class EstadoAberta(EstadoSolicitacao):
    """
    Primeiro estado do ciclo de vida: solicitação recém-criada.

    Neste estado a solicitação ainda não foi vista pelo setor acadêmico.
    O aluno possui plena autonomia para cancelá-la. Ao ser processada
    pelo serviço, avança para 'Em Análise'.

    Transições permitidas:
        - avancar() → EstadoEmAnalise
        - cancelar() → EstadoCancelada
    """

    def nome(self) -> str:
        """Retorna 'Aberta'."""
        return "Aberta"

    def avancar(self, solicitacao) -> None:
        """
        Transição: Aberta → Em Análise.

        Indica que o setor acadêmico recebeu e começou a analisar
        a solicitação.

        :param solicitacao: Objeto Solicitacao a ser avançado.
        """
        print("[Estado] Solicitação avançou para 'Em Análise'.")
        solicitacao._estado = EstadoEmAnalise()
        solicitacao.status = "Em Análise"

    def cancelar(self, solicitacao) -> None:
        """
        Transição: Aberta → Cancelada.

        O aluno pode cancelar livremente enquanto a solicitação
        ainda não entrou em análise.

        :param solicitacao: Objeto Solicitacao a ser cancelado.
        """
        print("[Estado] Solicitação cancelada pelo aluno.")
        solicitacao._estado = EstadoCancelada()
        solicitacao.status = "Cancelada"


class EstadoEmAnalise(EstadoSolicitacao):
    """
    Segundo estado: solicitação em verificação pelo setor acadêmico.

    O setor está avaliando os dados e as regras aplicáveis.
    O aluno não pode mais cancelar diretamente — deve solicitar ao setor.
    Ao concluir a análise, a solicitação pode ser aprovada ou rejeitada.

    Transições permitidas:
        - avancar() → EstadoFinalizada (status: 'Aprovada')
        - rejeitar() → EstadoFinalizada (status: 'Rejeitada') [via Solicitacao]

    Transições proibidas:
        - cancelar() → CancelamentoNaoPermitidoError
    """

    def nome(self) -> str:
        """Retorna 'Em Análise'."""
        return "Em Análise"

    def avancar(self, solicitacao) -> None:
        """
        Transição: Em Análise → Finalizada (Aprovada).

        Indica que o setor acadêmico analisou e aprovou a solicitação.

        :param solicitacao: Objeto Solicitacao a ser finalizado como aprovado.
        """
        print("[Estado] Solicitação finalizada e aprovada.")
        solicitacao._estado = EstadoFinalizada()
        solicitacao.status = "Aprovada"

    def cancelar(self, solicitacao) -> None:
        """
        Operação proibida neste estado.

        O aluno não pode cancelar uma solicitação que já está em análise.
        O cancelamento deve ser solicitado formalmente ao setor acadêmico.

        :raises CancelamentoNaoPermitidoError: sempre, ao ser chamado.
        """
        raise CancelamentoNaoPermitidoError("Em Análise")


class EstadoFinalizada(EstadoSolicitacao):
    """
    Estado terminal: solicitação aprovada ou rejeitada pelo setor.

    Uma solicitação finalizada é imutável — nenhuma ação posterior
    é permitida sobre ela. Isso implementa a regra de negócio de
    'imutabilidade pós-finalização'.

    Transições permitidas: nenhuma.
    Todas as ações levantam TransicaoEstadoInvalidaError.
    """

    def nome(self) -> str:
        """Retorna 'Finalizada'."""
        return "Finalizada"

    def avancar(self, solicitacao) -> None:
        """
        Operação proibida: solicitação finalizada é imutável.

        :raises TransicaoEstadoInvalidaError: sempre.
        """
        raise TransicaoEstadoInvalidaError("Finalizada", "avancar")

    def cancelar(self, solicitacao) -> None:
        """
        Operação proibida: solicitação finalizada é imutável.

        :raises TransicaoEstadoInvalidaError: sempre.
        """
        raise TransicaoEstadoInvalidaError("Finalizada", "cancelar")


class EstadoCancelada(EstadoSolicitacao):
    """
    Estado terminal: solicitação cancelada pelo aluno.

    Uma solicitação cancelada é imutável — assim como a Finalizada,
    não aceita nenhuma ação posterior.

    Transições permitidas: nenhuma.
    Todas as ações levantam TransicaoEstadoInvalidaError.
    """

    def nome(self) -> str:
        """Retorna 'Cancelada'."""
        return "Cancelada"

    def avancar(self, solicitacao) -> None:
        """
        Operação proibida: solicitação cancelada é imutável.

        :raises TransicaoEstadoInvalidaError: sempre.
        """
        raise TransicaoEstadoInvalidaError("Cancelada", "avancar")

    def cancelar(self, solicitacao) -> None:
        """
        Operação proibida: solicitação já está cancelada.

        :raises TransicaoEstadoInvalidaError: sempre.
        """
        raise TransicaoEstadoInvalidaError("Cancelada", "cancelar")
