from abc import ABC, abstractmethod

class EstadoSolicitacao(ABC):

    @abstractmethod
    def executar(self, solicitacao):
        pass


class EstadoAberta(EstadoSolicitacao):
    def executar(self, solicitacao):
        print("Estado: Aberta")
        solicitacao.alterar_estado(EstadoEmAnalise())


class EstadoEmAnalise(EstadoSolicitacao):
    def executar(self, solicitacao):
        print("Estado: Em Análise")
        solicitacao.alterar_estado(EstadoFinalizada())


class EstadoFinalizada(EstadoSolicitacao):
    def executar(self, solicitacao):
        print("Estado: Finalizada")
