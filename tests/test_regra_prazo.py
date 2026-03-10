import pytest
import datetime
from rules.regra_prazo import RegraPrazo
from domain.excecoes import ViolacaoRegraAcademicaError
from unittest.mock import MagicMock

#FIXTURES

@pytest.fixture
def regra():
    """Retorna uma instância da RegraPrazo."""
    return RegraPrazo()

@pytest.fixture
def solicitacao_mock():
    """Cria um mock básico para a solicitação."""
    return MagicMock()

#Dentro do Prazo

def test_deve_aprovar_solicitacao_dentro_do_prazo(regra, solicitacao_mock):
    """Verifica se aprova quando a data é anterior ou igual ao prazo."""
    # Data: 10/03/2026, Prazo: 15/03/2026
    solicitacao_mock.data = datetime.date(2026, 3, 10)
    solicitacao_mock.prazo = datetime.date(2026, 3, 15)
    
    assert regra.validar(solicitacao_mock) is True

def test_deve_aprovar_solicitacao_no_ultimo_dia_do_prazo(regra, solicitacao_mock):
    """Garante que a regra é inclusiva (data == prazo)."""
    hoje = datetime.date.today()
    solicitacao_mock.data = hoje
    solicitacao_mock.prazo = hoje
    
    assert regra.validar(solicitacao_mock) is True

#Fora do Prazo

def test_deve_lancar_erro_quando_prazo_vencido(regra, solicitacao_mock):
    """Valida se a exceção é lançada com a mensagem e formatação corretas."""
    # Data posterior ao prazo
    data_sol = datetime.date(2026, 3, 20)
    data_limite = datetime.date(2026, 3, 15)
    
    solicitacao_mock.data = data_sol
    solicitacao_mock.prazo = data_limite
    
    with pytest.raises(ViolacaoRegraAcademicaError) as excinfo:
        regra.validar(solicitacao_mock)
    
    # Verifica se a mensagem formatada em DD/MM/YYYY está correta
    assert "Prazo acadêmico encerrado" in str(excinfo.value)
    assert "Data da solicitação: 20/03/2026" in str(excinfo.value)
    assert "prazo limite: 15/03/2026" in str(excinfo.value)
    assert excinfo.value.regra == "RegraPrazo"

#TESTE DE ROBUSTEZ (Atributos Ausentes)

def test_deve_assumir_prazo_valido_se_atributos_ausentes(regra):
    """
    Testa o uso do getattr. Se a solicitação não tiver data/prazo, 
    deve usar hoje para ambos e retornar True.
    """
    solicitacao_vazia = MagicMock(spec=[]) # Mock sem nenhum atributo
    
    # Não deve levantar AttributeError
    assert regra.validar(solicitacao_vazia) is True