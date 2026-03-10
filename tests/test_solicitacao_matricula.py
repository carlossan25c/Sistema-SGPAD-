import pytest
from unittest.mock import MagicMock
from domain.solicitacao_matricula import SolicitacaoMatricula
from domain.estado import EstadoAberta

#FIXTURES

@pytest.fixture
def aluno_mock():
    return MagicMock()

@pytest.fixture
def disciplina_alvo():
    return MagicMock(nome="Cálculo II", carga_horaria=72)

@pytest.fixture
def co_requisito():
    return MagicMock(nome="Laboratório de Cálculo", carga_horaria=36)

#TESTES DE INICIALIZAÇÃO E ATRIBUTOS

def test_criacao_solicitacao_matricula_basica(aluno_mock, disciplina_alvo):
    """Verifica se a matrícula nasce com os dados básicos e estado inicial."""
    solicitacao = SolicitacaoMatricula(aluno=aluno_mock, disciplina=disciplina_alvo)
    
    assert solicitacao.aluno == aluno_mock
    assert solicitacao.disciplina == disciplina_alvo
    assert isinstance(solicitacao.estado_atual, EstadoAberta)
    # Deve iniciar com lista vazia de co-requisitos se não informada
    assert solicitacao.disciplinas_co_req_solicitadas == []
    # Deve iniciar com carga horária zero
    assert solicitacao.carga_horaria_semestre_atual == 0

def test_criacao_com_co_requisitos_simultaneos(aluno_mock, disciplina_alvo, co_requisito):
    """Garante que a lista de co-requisitos solicitados é armazenada corretamente."""
    solicitacao = SolicitacaoMatricula(
        aluno=aluno_mock, 
        disciplina=disciplina_alvo,
        disciplinas_co_req_solicitadas=[co_requisito]
    )
    
    assert len(solicitacao.disciplinas_co_req_solicitadas) == 1
    assert solicitacao.disciplinas_co_req_solicitadas[0].nome == "Laboratório de Cálculo"

#TESTES DE REGRAS ACADÊMICAS

def test_atribuicao_de_carga_horaria_externa(aluno_mock, disciplina_alvo):
    """
    Testa se o atributo opcional carga_horaria_semestre_atual pode ser 
    definido externamente para a RegraLimiteCargaHoraria.
    """
    solicitacao = SolicitacaoMatricula(aluno_mock, disciplina_alvo)
    solicitacao.carga_horaria_semestre_atual = 160
    
    assert solicitacao.carga_horaria_semestre_atual == 160

#TESTE DE REPRESENTAÇÃO (__STR__)

def test_representacao_str_matricula(aluno_mock, disciplina_alvo):
    """Valida se o formato da string de matrícula segue o padrão da classe base."""
    aluno_mock.nome = "Ana Lima"
    solicitacao = SolicitacaoMatricula(aluno_mock, disciplina_alvo)
    
    resultado = str(solicitacao)
    assert "Solicitação de SolicitacaoMatricula" in resultado
    assert "Aluno: Ana Lima" in resultado
    assert "Disciplina: Cálculo II" in resultado
    assert "Status: Aberta" in resultado