from domain.professor import Professor
from domain.disciplina import Disciplina

def test_professor_e_suas_disciplinas():

    professor = Professor(nome="Davi", email="davi@ufca.edu.br", siape="1234567")
    disciplina = Disciplina(codigo="POO01", carga_horaria=64)
    
    professor.adicionar_disciplina(disciplina)
    
    assert professor.nome == "Davi"
    assert professor._siape == "1234567"
    assert len(professor._disciplinas) == 1
    assert professor._disciplinas[0].codigo == "POO01"