import pytest
from domain.aluno import Aluno
from domain.curso import Curso
from domain.historico import Historico

#FIXTURES (Para evitar repetição de código)

@pytest.fixture
def curso_medicina():
    """Cria um objeto Curso padrão para os testes."""
    return Curso(nome="Medicina", limite_horas_semestrais=400)

@pytest.fixture
def aluno_padrao(curso_medicina):
    """Cria um objeto Aluno padrão para os testes."""
    return Aluno(
        nome="Carlos Santos", 
        email="carlos@ufca.edu.br", 
        matricula="2026001", 
        curso=curso_medicina
    )

#TESTES DE HERANÇA E IDENTIDADE

def test_aluno_deve_herdar_id_do_identifiable_mixin(aluno_padrao):
    """Verifica se o Mixin está gerando UUIDs únicos corretamente."""
    assert aluno_padrao.id is not None
    assert isinstance(aluno_padrao.id, str)
    assert len(aluno_padrao.id) > 30  # Formato UUID

def test_aluno_deve_herdar_dados_do_usuario(aluno_padrao):
    """Garante que o Aluno respeita o contrato da classe Usuario."""
    assert aluno_padrao.nome == "Carlos Santos"
    assert aluno_padrao.email == "carlos@ufca.edu.br"

#TESTES DE ENCAPSULAMENTO E PROTEÇÃO

def test_matricula_deve_ser_imutavel(aluno_padrao):
    """A matrícula é a chave do aluno na UFCA e não pode ser alterada."""
    with pytest.raises(AttributeError):
        aluno_padrao.matricula = "2026999"

def test_validacao_de_tipo_no_setter_do_curso(aluno_padrao):
    """O sistema deve impedir que o curso seja substituído por algo que não seja Curso."""
    with pytest.raises(TypeError) as excinfo:
        aluno_padrao.curso = "Engenharia Civil" # String em vez de objeto Curso
    
    assert "Curso deve ser um objeto da classe Curso" in str(excinfo.value)

def test_encapsulamento_da_lista_de_pendencias(aluno_padrao):
    """Garante que a lista de pendências só mude através dos métodos oficiais."""
    aluno_padrao.adicionar_pendencia("Foto 3x4 pendente")
    
    # Tenta burlar adicionando na cópia retornada pela property
    aluno_padrao.pendencias.append("Invasão")
    
    # A lista real deve permanecer com apenas 1 item
    assert len(aluno_padrao._pendencias) == 1

#TESTES DE REGRAS DE NEGÓCIO (PENDÊNCIAS)

def test_fluxo_completo_de_pendencias(aluno_padrao):
    """Testa o ciclo de vida das pendências documentais."""
    # Estado inicial
    assert not aluno_padrao.tem_pendencias()
    
    # Adicionando
    aluno_padrao.adicionar_pendencia("Débito Biblioteca")
    assert aluno_padrao.tem_pendencias() is True
    
    # Removendo
    aluno_padrao.remover_pendencia("Débito Biblioteca")
    assert not aluno_padrao.tem_pendencias()

def test_remover_pendencia_inexistente_nao_deve_gerar_erro(aluno_padrao):
    """O método deve ser silencioso se tentar remover algo que não existe."""
    aluno_padrao.remover_pendencia("Algo que nunca existiu")
    assert not aluno_padrao.tem_pendencias()

#TESTE DE REPRESENTAÇÃO

def test_representacao_textual_do_aluno(aluno_padrao):
    """Valida se o formato do __str__ está de acordo com o padrão institucional."""
    esperado = "Aluno: Carlos Santos (2026001) - Curso: Medicina"
    assert str(aluno_padrao) == esperado