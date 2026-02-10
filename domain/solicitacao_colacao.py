from domain.solicitacao import Solicitacao

class SolicitacaoColacao(Solicitacao):
    def __init__(self, aluno, curso):
        super().__init__(aluno)
        self._curso = curso

    def validar(self):
        return True
