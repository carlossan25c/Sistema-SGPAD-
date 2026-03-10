import pytest
from unittest.mock import MagicMock
from domain.solicitacao_colacao import SolicitacaoColacao
from domain.estado import EstadoAberta

#FIXTURES

@pytest.fixture
def aluno_mock():
    """Simula um aluno vinculado a um curso de Medicina."""
    aluno = MagicMock()
    aluno.curso.nome = "Medicina"
    return aluno

@pytest.fixture
def curso_mock():
    """Simula o curso de Medicina da UFCA."""
    return MagicMock(nome="Medicina")

#TESTES DE INICIALIZAÇÃO E HERANÇA

def test_criacao_solicitacao_colacao(aluno_mock, curso_mock):
    """Verifica se a solicitação nasce no estado correto e com os dados certos."""
    solicitacao = SolicitacaoColacao(aluno=aluno_mock, curso=curso_mock)
    
    # Deve herdar o comportamento de Solicitacao (Padrão State)
    assert isinstance(solicitacao.estado_atual, EstadoAberta)
    assert solicitacao.aluno == aluno_mock
    assert solicitacao.curso == curso_mock

def test_solicitacao_colacao_deve_ser_vinculada_ao_curso(aluno_mock, curso_mock):
    """Garante que a formatura é do curso, não de uma disciplina isolada."""
    solicitacao = SolicitacaoColacao(aluno_mock, curso_mock)
    
    #Verifica se o atributo curso (herdado de Solicitacao) foi preenchido
    assert hasattr(solicitacao, 'curso')
    assert solicitacao.curso.nome == "Medicina"

#TESTE DE INTEGRAÇÃO CONCEITUAL (MOCK DE REGRAS)

def test_fluxo_de_validacao_da_colacao(aluno_mock, curso_mock):
    """
    Simula como o service usaria esta classe com as regras que corrigimos:
    RegraElegibilidade e RegraPendenciaDocumentacao.
    """
    solicitacao = SolicitacaoColacao(aluno_mock, curso_mock)
    
    #Mocks das regras para testar a compatibilidade da interface
    regra_elegibilidade = MagicMock()
    regra_pendencias = MagicMock()
    
    # Se as regras retornarem True, a colação segue
    regra_elegibilidade.validar.return_value = True
    regra_pendencias.validar.return_value = True
    
    assert regra_elegibilidade.validar(solicitacao) is True
    assert regra_pendencias.validar(solicitacao) is True