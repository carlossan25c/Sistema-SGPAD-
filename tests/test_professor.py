from domain.professor import Professor
from domain.disciplina import Disciplina
import pytest
from domain.professor import Professor
from domain.disciplina import Disciplina

#FIXTURES

@pytest.fixture
def prof_doutor():
    """Cria um professor para os testes."""
    return Professor("Dr. Rafael Souza", "rafael@ufca.edu.br", "1234567")

@pytest.fixture
def disciplina_poo():
    """Cria uma disciplina para vincular ao professor."""
    return Disciplina(nome="POO", carga_horaria=60, codigo="INF001")

#TESTES DE HERANÇA E INICIALIZAÇÃO

def test_professor_deve_herdar_dados_de_usuario(prof_doutor):
    """Garante que o Professor herda corretamente o contrato de Usuario."""
    assert prof_doutor.nome == "Dr. Rafael Souza"
    assert prof_doutor.email == "rafael@ufca.edu.br"

def test_siape_deve_ser_somente_leitura(prof_doutor):
    """O SIAPE é o ID funcional e não deve ser alterado após a criação."""
    assert prof_doutor.siape == "1234567"
    with pytest.raises(AttributeError):
        prof_doutor.siape = "7654321"

#TESTES DE GESTÃO DE DISCIPLINAS

def test_adicionar_disciplina_ao_professor(prof_doutor, disciplina_poo):
    """Verifica se o vínculo entre professor e matéria funciona."""
    prof_doutor.adicionar_disciplina(disciplina_poo)
    
    assert len(prof_doutor.disciplinas) == 1
    assert prof_doutor.disciplinas[0].nome == "POO"

def test_protecao_da_lista_de_disciplinas_do_professor(prof_doutor, disciplina_poo):
    """
    Garante que a lista interna do professor esteja protegida contra 
    modificações externas via cópia.
    """
    prof_doutor.adicionar_disciplina(disciplina_poo)
    
    # Tenta burlar a lista usando a propriedade
    prof_doutor.disciplinas.append(Disciplina(nome="Disciplina Invasora"))
    
    # A lista real deve continuar com apenas 1 item
    assert len(prof_doutor._disciplinas) == 1