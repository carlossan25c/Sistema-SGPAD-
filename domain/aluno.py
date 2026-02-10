from domain.usuario import Usuario
from domain.curso import Curso
from domain.historico import Historico

class Aluno(Usuario):
    def __init__(self, nome: str, email: str, matricula: str, curso: Curso):
        super().__init__(nome, email)
        self._matricula = matricula
        self._curso = curso
        self._historico = Historico()

    @property
    def matricula(self):
        return self._matricula

    @property
    def curso(self):
        return self._curso

    @property
    def historico(self):
        return self._historico
