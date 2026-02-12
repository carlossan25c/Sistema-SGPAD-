# domain/solicitacao.py
class Solicitacao:
    def __init__(self, aluno, disciplina=None, curso=None):
        self.aluno = aluno
        self.disciplina = disciplina
        self.curso = curso
        self.status = "Aberta"

    def aprovar(self):
        self.status = "Aprovada"

    def rejeitar(self):
        self.status = "Rejeitada"

    def __str__(self):
        if self.disciplina:
            return f"Solicitação de {self.__class__.__name__} - Aluno: {self.aluno.nome}, Disciplina: {self.disciplina.nome}, Status: {self.status}"
        elif self.curso:
            return f"Solicitação de {self.__class__.__name__} - Aluno: {self.aluno.nome}, Curso: {self.curso.nome}, Status: {self.status}"
        else:
            return f"Solicitação de {self.__class__.__name__} - Aluno: {self.aluno.nome}, Status: {self.status}"
