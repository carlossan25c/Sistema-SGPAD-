from domain.solicitacao_matricula import SolicitacaoMatricula
from unittest.mock import MagicMock

def test_solicitacao_matricula_deve_iniciar_corretamente():
    
    aluno_mock = MagicMock()
    disciplina_mock = MagicMock()
    
    
    solicitacao = SolicitacaoMatricula(aluno=aluno_mock, disciplina=disciplina_mock)
    
    
    assert solicitacao.status == "Aberta"
    assert solicitacao._disciplina == disciplina_mock
    assert solicitacao.validar() is True