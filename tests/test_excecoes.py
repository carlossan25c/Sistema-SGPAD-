import pytest
from unittest.mock import MagicMock
import datetime

# Importação das exceções reais do seu projeto
from domain.excecoes import (
    ViolacaoRegraAcademicaError, 
    TransicaoEstadoInvalidaError, 
    CancelamentoNaoPermitidoError
)

#TESTES DE REGRAS ACADÊMICAS

def test_excecao_regra_prazo_expirado():
    """Valida se o erro de prazo carrega a mensagem e o nome da regra corretamente."""
    mensagem_erro = "Prazo acadêmico encerrado. Limite era 15/02/2026."
    
    with pytest.raises(ViolacaoRegraAcademicaError) as excinfo:
        raise ViolacaoRegraAcademicaError(mensagem=mensagem_erro, regra="RegraPrazo")
    
    #Verifica a formatação do __str__ personalizada que você criou
    assert "[Violação Acadêmica - RegraPrazo]" in str(excinfo.value)
    assert mensagem_erro in str(excinfo.value)

def test_excecao_regra_creditos_insuficientes():
    """Valida o erro quando o aluno não atinge o mínimo de créditos."""
    with pytest.raises(ViolacaoRegraAcademicaError) as excinfo:
        raise ViolacaoRegraAcademicaError(
            mensagem="Aluno possui apenas 50h de 120h necessárias.",
            regra="RegraElegibilidade"
        )
    assert "RegraElegibilidade" in str(excinfo.value)

#ESTES DE FLUXO E ESTADOS

def test_excecao_transicao_invalida_em_estado_terminal():
    """Garante que o erro de transição descreva corretamente o estado e a ação."""
    estado = "Finalizada"
    acao = "avancar"
    
    with pytest.raises(TransicaoEstadoInvalidaError) as excinfo:
        raise TransicaoEstadoInvalidaError(estado_atual=estado, acao=acao)
    
    #Verifica se a mensagem montada no __init__ da exceção está correta
    assert "[Transição Inválida]" in str(excinfo.value)
    assert f"Ação '{acao}' não permitida no estado '{estado}'" in str(excinfo.value)

def test_excecao_cancelamento_negado_pela_ufca():
    """Valida a regra de que o aluno não cancela processos em análise."""
    with pytest.raises(CancelamentoNaoPermitidoError) as excinfo:
        raise CancelamentoNaoPermitidoError(estado_atual="Em Análise")
    
    assert "[Cancelamento Negado]" in str(excinfo.value)
    assert "solicite o cancelamento ao Setor Acadêmico" in str(excinfo.value)

#TESTE DE INTEGRAÇÃO COM MOCK

def test_regra_disparando_excecao_no_fluxo():
    """Simula uma classe de regra real disparando a exceção capturada pelo teste."""
    regra_mock = MagicMock()
    
    regra_mock.validar.side_effect = ViolacaoRegraAcademicaError("Erro de teste", "RegraMock")
    
    with pytest.raises(ViolacaoRegraAcademicaError):
        regra_mock.validar(MagicMock())