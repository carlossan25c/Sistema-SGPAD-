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
        return self.__matricula
    
    @matricula.setter
    def matricula(self, nova_matricula):
        if isinstance(nova_matricula, str):
            self.__matricula = nova_matricula

        else:
            raise TypeError("Matricula deve ser String!")
        

    @property
    def curso(self):
        return self.__curso

    @curso.setter
    def curso(self, novo_curso):
        if not isinstance(novo_curso, str):
            raise TypeError("Curso deve ser String!")
        
        if not isinstance(novo_curso, Curso):
            raise TypeError("Esperava instância de curso.")
        
        else:
            self.__curso = novo_curso
        

    @property
    def historico(self):
        return self._historico
