import pytest
from domain.aluno import Aluno
from domain.curso import Curso

def test_aluno_deve_ser_inicializado_com_historico_vazio():
    
    meu_curso = Curso(nome="Engenharia de Software")
    aluno = Aluno(nome="Davi", email="davi@email.com", matricula="2024001", curso=meu_curso)

    assert aluno.historico is not None
    assert aluno.historico.total_creditos() == 0