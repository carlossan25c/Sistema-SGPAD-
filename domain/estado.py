from abc import ABC, abstractmethod

class EstadoSolicitacao(ABC):
    """
    Interface base para o padrão de projeto State.
    Define o comportamento comum para diferentes fases de uma solicitação.
    """

    @abstractmethod
    def executar(self, solicitacao):
        pass


class EstadoAberta(EstadoSolicitacao):
    def executar(self, solicitacao):
        print("Estado: Aberta")
        solicitacao.alterar_estado(EstadoEmAnalise())
        """Primeira fase: Solicitação recém-criada."""


class EstadoEmAnalise(EstadoSolicitacao):
    def executar(self, solicitacao):
        print("Estado: Em Análise")
        solicitacao.alterar_estado(EstadoFinalizada())
        """Segunda fase: A solicitação está sendo verificada por um setor."""


class EstadoFinalizada(EstadoSolicitacao):
    def executar(self, solicitacao):
        print("Estado: Finalizada")
        """Fase Final: Ciclo de vida encerrado."""
