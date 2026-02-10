import pytest
from domain.curso import Curso
from domain.disciplina import Disciplina

def test_adicionar_disciplina_ao_curso():
    
    disciplina = Disciplina(codigo="POO001", carga_horaria=60)
    curso = Curso(nome="Engenharia de Software")
    
    curso.disciplinas.append(disciplina)
    assert len(curso.disciplinas) == 1