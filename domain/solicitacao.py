from abc import ABC, abstractmethod

class Solicitacao(ABC):
    def __init__(self, aluno):
        self._aluno = aluno
        self._status = "Aberta"

    @property
    def aluno(self):
        return self._aluno

    @property
    def status(self):
        return self._status

    def mudar_estado(self, novo_estado: str):
        if self._status == "Finalizada" and novo_estado == "Aberta":
            raise ValueError("Não é possível reabrir solicitação finalizada.")
        self._status = novo_estado

    @abstractmethod
    def validar(self):
        pass
