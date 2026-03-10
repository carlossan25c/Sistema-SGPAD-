import pytest
import datetime
from unittest.mock import MagicMock
from domain.solicitacao_trancamento import SolicitacaoTrancamento
from domain.estado import EstadoAberta

#FIXTURES

@pytest.fixture
def aluno_mock():
    return MagicMock()

@pytest.fixture
def disciplina_mock():
    return MagicMock(nome="Bioquímica")

#TESTES DE INICIALIZAÇÃO

def test_criacao_solicitacao_trancamento_com_datas_padrao(aluno_mock, disciplina_mock):
    """Verifica se a solicitação assume a data de hoje quando omitida."""
    solicitacao = SolicitacaoTrancamento(aluno=aluno_mock, disciplina=disciplina_mock)
    
    hoje = datetime.date.today()
    assert solicitacao.data == hoje
    assert solicitacao.prazo == hoje
    assert isinstance(solicitacao.estado_atual, EstadoAberta)

def test_criacao_com_datas_especificas(aluno_mock, disciplina_mock):
    """Garante que as datas injetadas são preservadas para a RegraPrazo."""
    data_envio = datetime.date(2026, 3, 10)
    data_limite = datetime.date(2026, 3, 20)
    
    solicitacao = SolicitacaoTrancamento(
        aluno=aluno_mock, 
        disciplina=disciplina_mock,
        data=data_envio,
        prazo=data_limite
    )
    
    assert solicitacao.data == data_envio
    assert solicitacao.prazo == data_limite

#TESTES DE INTEGRAÇÃO COM REGRAS

def test_compatibilidade_com_regra_prazo(aluno_mock, disciplina_mock):
    """
    Verifica se a solicitação possui os atributos que a RegraPrazo exige 
    para não disparar o getattr de fallback.
    """
    solicitacao = SolicitacaoTrancamento(aluno_mock, disciplina_mock)
    
    # A RegraPrazo fará: getattr(solicitacao, "data")
    assert hasattr(solicitacao, "data")
    assert hasattr(solicitacao, "prazo")

#REPRESENTAÇÃO E HERANÇA

def test_representacao_str_trancamento(aluno_mock, disciplina_mock):
    """Valida se a string identifica corretamente o tipo de solicitação."""
    aluno_mock.nome = "Carlos Santos"
    solicitacao = SolicitacaoTrancamento(aluno_mock, disciplina_mock)
    
    resultado = str(solicitacao)
    assert "Solicitação de SolicitacaoTrancamento" in resultado
    assert "Disciplina: Bioquímica" in resultado