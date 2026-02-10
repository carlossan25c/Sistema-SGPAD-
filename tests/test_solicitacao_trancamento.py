from domain.solicitacao_trancamento import SolicitacaoTrancamento
from unittest.mock import MagicMock

def test_solicitacao_trancamento_deve_vincular_disciplina_corretamente():
    
    aluno_mock = MagicMock()
    disciplina_mock = MagicMock()
    
    solicitacao = SolicitacaoTrancamento(aluno=aluno_mock, disciplina=disciplina_mock)
    
    assert solicitacao.status == "Aberta"
    assert solicitacao._disciplina == disciplina_mock
    assert solicitacao.validar() is True