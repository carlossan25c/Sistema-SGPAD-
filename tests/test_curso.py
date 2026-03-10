import pytest
from domain.curso import Curso
from domain.disciplina import Disciplina

def test_criacao_curso_com_valores_padrao():
    
    curso = Curso(nome="Medicina")
    
    assert curso.nome == "Medicina"
    assert curso.limite_horas_semestrais == 360
    assert curso.min_horas_optativas == 0
    assert len(curso.disciplinas) == 0

def test_adicionar_disciplina_com_sucesso():
    """Verifica se o método adicionar_disciplina funciona corretamente."""
    curso = Curso(nome="Medicina")
    anatomia = Disciplina(nome="Anatomia I", carga_horaria=80, obrigatoria=True)
    
    curso.adicionar_disciplina(anatomia)
    
    assert len(curso.disciplinas) == 1
    assert curso.disciplinas[0].nome == "Anatomia I"

def test_evitar_disciplina_duplicada():
    """Garante que a mesma disciplina não seja cadastrada duas vezes no currículo."""
    curso = Curso(nome="Medicina")
    bioquimica = Disciplina(nome="Bioquímica", carga_horaria=60)
    
    curso.adicionar_disciplina(bioquimica)
    curso.adicionar_disciplina(bioquimica) #Tentativa duplicada
    
    assert len(curso.disciplinas) == 1

def test_encapsulamento_da_lista_de_disciplinas():
    """
    Verifica se a lista de disciplinas está protegida. 
    Modificar a cópia retornada pela propriedade não deve afetar o curso.
    """
    curso = Curso(nome="Medicina")
    curso.adicionar_disciplina(Disciplina(nome="Histologia", carga_horaria=40))
    
    #Tenta burlar o encapsulamento
    lista_externa = curso.disciplinas
    lista_externa.append(Disciplina(nome="Disciplina Invasora", carga_horaria=0))
    
    #O curso deve permanecer íntegro com apenas 1 disciplina
    assert len(curso.disciplinas) == 1

def test_filtragem_de_disciplinas_obrigatorias():
    """Valida se o método disciplinas_obrigatorias separa corretamente a grade."""
    curso = Curso(nome="Medicina")
    d1 = Disciplina(nome="Semiologia", carga_horaria=100, obrigatoria=True)
    d2 = Disciplina(nome="Libras", carga_horaria=40, obrigatoria=False)
    
    curso.adicionar_disciplina(d1)
    curso.adicionar_disciplina(d2)
    
    obrigatorias = curso.disciplinas_obrigatorias()
    
    assert len(obrigatorias) == 1
    assert obrigatorias[0].nome == "Semiologia"
    assert obrigatorias[0].obrigatoria is True

def test_representacao_em_string():
    """Testa o método __str__ para logs e interface."""
    curso = Curso(nome="Medicina")
    assert str(curso) == "Curso: Medicina"