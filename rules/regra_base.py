from abc import ABC, abstractmethod

class Regra(ABC):
    """
    Interface abstrata que define o contrato para todas as regras acadêmicas.
    Implementa o padrão Strategy.
    """
    @abstractmethod
    def validar(self, solicitacao):
        pass
    """
        Método obrigatório que deve retornar True se a solicitação cumpre os requisitos.
        
        :param solicitacao: Objeto do tipo Solicitacao a ser analisado.
        """
