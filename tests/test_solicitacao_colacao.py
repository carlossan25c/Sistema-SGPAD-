from domain.solicitacao_colacao import SolicitacaoColacao
from unittest.mock import MagicMock

def test_solicitacao_colacao_inicializacao():
    
    aluno_mock = MagicMock()
    curso_mock = MagicMock()
    
    
    solicitacao = SolicitacaoColacao(aluno=aluno_mock, curso=curso_mock)
    
    
    assert solicitacao.status == "Aberta"  
    assert solicitacao._curso == curso_mock
    assert solicitacao.validar() is True