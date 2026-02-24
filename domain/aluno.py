# domain/aluno.py
from domain.curso import Curso
from domain.historico import Historico

class Aluno:
    """
    Representa o estudante no sistema. 
    Gerencia dados cadastrais, vínculo com curso e histórico acadêmico.
    """
    def __init__(self, nome: str, email: str, matricula: str, curso: Curso):
        self.nome = nome
        self.email = email
        self.__matricula = matricula
        self.__curso = curso
        self.historico = Historico()

    @property
    def matricula(self):
        return self.__matricula
    """Getter para acesso seguro à matrícula."""

    @property
    def curso(self):
        return self.__curso
    """Getter para acesso ao objeto Curso."""

    @curso.setter
    def curso(self, value):
        """Valida se o valor atribuído é de fato uma instância da classe Curso."""
        if not isinstance(value, Curso):
            raise TypeError("Curso deve ser um objeto da classe Curso!")
        self.__curso = value

    def __str__(self):
        return f"Aluno: {self.nome} ({self.matricula}) - Curso: {self.curso.nome}"
