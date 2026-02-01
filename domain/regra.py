from abc import ABC, abstractmethod

class RegraSolicitacao(ABC):

    @abstractmethod
    def avaliar(self, solicitacao) -> bool:
        pass


class RegraPrazo(RegraSolicitacao):
    def avaliar(self, solicitacao) -> bool:
        print("Regra de prazo aplicada")
        return True


class RegraElegibilidade(RegraSolicitacao):
    def avaliar(self, solicitacao) -> bool:
        print("Regra de elegibilidade aplicada")
        return True
