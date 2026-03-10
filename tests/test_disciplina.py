import pytest
from domain.disciplina import Disciplina

#FIXTURES

@pytest.fixture
def calc1():
    return Disciplina(nome="Cálculo I", carga_horaria=72, codigo="MAT001")

@pytest.fixture
def calc2():
    return Disciplina(nome="Cálculo II", carga_horaria=72, codigo="MAT002")

@pytest.fixture
def fisica_lab():
    return Disciplina(nome="Física Experimental", carga_horaria=40, obrigatoria=False)

#TESTES DE INICIALIZAÇÃO

def test_criacao_disciplina_com_parametros_completos(calc1):
    """Verifica se os atributos básicos são atribuídos corretamente."""
    assert calc1.nome == "Cálculo I"
    assert calc1.carga_horaria == 72
    assert calc1.codigo == "MAT001"
    assert calc1.obrigatoria is True

def test_fallback_nome_e_codigo():
    """Testa a lógica de fallback quando nome ou código são omitidos."""
    # Apenas código informado -> Nome assume o código
    d1 = Disciplina(codigo="INF01", carga_horaria=60)
    assert d1.nome == "INF01"
    
    # Nada informado
    d2 = Disciplina()
    assert d2.nome == "Sem nome"
    assert d2.carga_horaria == 0

#TESTES DE RELACIONAMENTOS (PRÉ E CO-REQUISITOS)

def test_fluxo_de_pre_requisitos(calc1, calc2):
    """Valida a adição e o encapsulamento de pré-requisitos."""
    calc2.adicionar_pre_requisito(calc1)
    
    # Verifica se foi adicionado
    assert calc1 in calc2.pre_requisitos
    assert len(calc2.pre_requisitos) == 1
    
    # Testar duplicata (deve ignorar silenciosamente)
    calc2.adicionar_pre_requisito(calc1)
    assert len(calc2.pre_requisitos) == 1
    
    # Testar proteção da lista (cópia)
    calc2.pre_requisitos.append(Disciplina(nome="Invasora"))
    assert len(calc2._pre_requisitos) == 1

def test_fluxo_de_co_requisitos(calc1, fisica_lab):
    """Valida a adição de disciplinas simultâneas (co-requisitos)."""
    calc1.adicionar_co_requisito(fisica_lab)
    assert fisica_lab in calc1.co_requisitos
    assert len(calc1.co_requisitos) == 1

#TESTES DE IGUALDADE E HASH

def test_igualdade_entre_disciplinas():
    """Disciplinas com mesmo nome devem ser consideradas iguais (__eq__)."""
    d1 = Disciplina(nome="POO", carga_horaria=60)
    d2 = Disciplina(nome="POO", carga_horaria=80) # CH diferente, mas mesmo nome
    
    assert d1 == d2
    assert d1 != "POO" # Comparação com outro tipo

def test_uso_como_chave_em_dicionario(calc1):
    """Garante que a disciplina possa ser usada como chave no Histórico (__hash__)."""
    historico_notas = {calc1: 9.5}
    assert historico_notas[calc1] == 9.5
    
    # Mesma disciplina criada novamente deve acessar a mesma chave
    calc1_clone = Disciplina(nome="Cálculo I")
    assert historico_notas[calc1_clone] == 9.5

#TESTES DE REPRESENTAÇÃO

def test_representacao_str_e_repr(calc1):
    """Valida as saídas de texto para logs e interface."""
    assert str(calc1) == "Disciplina: Cálculo I (72h)"
    assert "Disciplina(nome='Cálculo I', carga_horaria=72)" in repr(calc1)