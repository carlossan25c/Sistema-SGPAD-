class Aluno:
    def __init__(self, matricula: str, nome: str, curso: str):
        self._matricula = matricula
        self._nome = nome
        self._curso = curso

    @property
    def matricula(self):
        return self._matricula

    @property
    def nome(self):
        return self._nome

    @property
    def curso(self):
        return self._curso
