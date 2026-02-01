from abc import ABC
from domain.estado import EstadoAberta
from domain.regra import RegraSolicitacao

class SolicitacaoAcademica(ABC):

    def __init__(self, aluno, setor):
        self._aluno = aluno
        self._setor = setor
        self._estado = EstadoAberta()
        self._regras: list[RegraSolicitacao] = []

    def adicionar_regra(self, regra: RegraSolicitacao):
        self._regras.append(regra)

    def alterar_estado(self, novo_estado):
        self._estado = novo_estado

    def executar(self):
        for regra in self._regras:
            if not regra.avaliar(self):
                print("Solicitação rejeitada")
                return
        self._estado.executar(self)


class SolicitacaoTrancamento(SolicitacaoAcademica):
    pass


class SolicitacaoDeclaracao(SolicitacaoAcademica):
    pass


class SolicitacaoRevisaoNota(SolicitacaoAcademica):
    pass
