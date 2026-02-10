from domain.historico import Historico
from domain.disciplina import Disciplina

def test_soma_total_creditos_real():
    
    historico = Historico()
    
    d1 = Disciplina(codigo="MAT01", carga_horaria=60)
    d2 = Disciplina(codigo="POO02", carga_horaria=40)
    
    historico.adicionar_disciplina(d1, 9.5)
    historico.adicionar_disciplina(d2, 8.0)
    
    assert historico.total_creditos() == 100