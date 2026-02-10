from rules.regra_prazo import RegraPrazo
from unittest.mock import MagicMock
import datetime

def test_solicitacao_dentro_do_prazo_deve_ser_valida():
    regra = RegraPrazo()
    solicitacao = MagicMock()
    
    solicitacao.data = datetime.date(2026, 2, 10)
    solicitacao.prazo = datetime.date(2026, 2, 15) 
    
    assert regra.validar(solicitacao) is True

def test_solicitacao_fora_do_prazo_deve_ser_invalida():
    regra = RegraPrazo()
    solicitacao = MagicMock()
    
    solicitacao.data = datetime.date(2026, 2, 20) 
    solicitacao.prazo = datetime.date(2026, 2, 15)
    
    assert regra.validar(solicitacao) is False