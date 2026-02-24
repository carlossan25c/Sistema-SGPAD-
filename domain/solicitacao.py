# domain/solicitacao.py
class Solicitacao:
    """
    Classe base (Superclasse) para todos os tipos de pedidos acadêmicos.
    Centraliza os dados básicos: aluno, alvo (disciplina/curso) e status.
    """
    def __init__(self, aluno, disciplina=None, curso=None):
        self.aluno = aluno
        self.disciplina = disciplina
        self.curso = curso
        self.status = "Aberta"

    def aprovar(self):
        self.status = "Aprovada"
        """Define o status como Aprovada."""

    def rejeitar(self):
        self.status = "Rejeitada"
        """Define o status como Rejeitada."""

    def __str__(self):
        """Retorna uma representação textual detalhada baseada no tipo de alvo."""
        if self.disciplina:
            return f"Solicitação de {self.__class__.__name__} - Aluno: {self.aluno.nome}, Disciplina: {self.disciplina.nome}, Status: {self.status}"
        elif self.curso:
            return f"Solicitação de {self.__class__.__name__} - Aluno: {self.aluno.nome}, Curso: {self.curso.nome}, Status: {self.status}"
        else:
            return f"Solicitação de {self.__class__.__name__} - Aluno: {self.aluno.nome}, Status: {self.status}"
