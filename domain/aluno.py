# domain/aluno.py
from domain.curso import Curso
from domain.historico import Historico

class Aluno:
    def __init__(self, nome: str, email: str, matricula: str, curso: Curso):
        self.nome = nome
        self.email = email
        self.__matricula = matricula
        self.__curso = curso
        self.historico = Historico()

    @property
    def matricula(self):
        return self.__matricula

    @property
    def curso(self):
        return self.__curso

    @curso.setter
    def curso(self, value):
        if not isinstance(value, Curso):
            raise TypeError("Curso deve ser um objeto da classe Curso!")
        self.__curso = value

    def __str__(self):
        return f"Aluno: {self.nome} ({self.matricula}) - Curso: {self.curso.nome}"
