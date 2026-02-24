from rules.regra_elegibilidade import RegraElegibilidade
from unittest.mock import MagicMock

def test_aluno_deve_ter_minimo_de_80_creditos():
    regra = RegraElegibilidade()
    solicitacao = MagicMock()
    """
    Valida a Regra de Elegibilidade (Pattern Strategy).
    Verifica se a regra aprova alunos com >= 80 créditos e reprova os demais.
    """
    
    # Simula aluno com 100 créditos (Elegível)
    solicitacao.aluno.historico.total_creditos.return_value = 100
    assert regra.validar(solicitacao) is True
    
    # Simula aluno com 50 créditos (Não elegível)
    solicitacao.aluno.historico.total_creditos.return_value = 50
    assert regra.validar(solicitacao) is False