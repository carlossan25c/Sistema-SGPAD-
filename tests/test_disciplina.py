from domain.disciplina import Disciplina

def test_dados_disciplina():
    
    disciplina = Disciplina(codigo= "POO01", carga_horaria=64)
    
    assert disciplina.carga_horaria == 64
    assert isinstance(disciplina.carga_horaria, int)