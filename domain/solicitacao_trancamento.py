from domain.solicitacao import Solicitacao

class SolicitacaoTrancamento(Solicitacao):
    def __init__(self, aluno, disciplina):
        super().__init__(aluno)
        self._disciplina = disciplina

    def validar(self):
        return True  # lógica simplificada
