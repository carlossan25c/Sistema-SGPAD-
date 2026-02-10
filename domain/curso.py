class Curso:
    def __init__(self, nome: str):
        self._nome = nome
        self._disciplinas = []

    def adicionar_disciplina(self, disciplina):
        self._disciplinas.append(disciplina)

    @property
    def disciplinas(self):
        return self._disciplinas
