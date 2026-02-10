from domain.usuario import Usuario

class Professor(Usuario):
    def __init__(self, nome: str, email: str, siape: str):
        super().__init__(nome, email)
        self._siape = siape
        self._disciplinas = []

    def adicionar_disciplina(self, disciplina):
        self._disciplinas.append(disciplina)
