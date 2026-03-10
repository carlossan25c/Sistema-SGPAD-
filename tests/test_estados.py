import pytest
from domain.estado import (
    EstadoAberta, 
    EstadoEmAnalise, 
    EstadoFinalizada, 
    EstadoCancelada
)
from domain.excecoes import (
    TransicaoEstadoInvalidaError, 
    CancelamentoNaoPermitidoError
)

class MockSolicitacao:
    """Simula a Solicitacao para testar a troca de estados internos."""
    def __init__(self):
        self._estado = EstadoAberta()
        self.status = "Aberta"

    @property
    def estado_atual(self):
        return self._estado

    def alterar_estado(self, novo_estado):
        self._estado = novo_estado

#TESTES DE SINCRONIZAÇÃO E NOMENCLATURA

def test_sincronizacao_de_status_texto_e_objeto():
    """Garante que ao mudar o objeto de estado, o atributo 'status' mude junto."""
    solicitacao = MockSolicitacao()
    
    #Transição: Aberta -> Em Análise
    solicitacao.estado_atual.avancar(solicitacao)
    assert isinstance(solicitacao.estado_atual, EstadoEmAnalise)
    assert solicitacao.status == "Em Análise"
    
    #Transição: Em Análise -> Finalizada (Aprovada)
    solicitacao.estado_atual.avancar(solicitacao)
    assert isinstance(solicitacao.estado_atual, EstadoFinalizada)
    assert solicitacao.status == "Aprovada"

def test_nomes_textuais_dos_estados():
    """Valida se as strings de retorno para a UI estão corretas."""
    assert EstadoAberta().nome() == "Aberta"
    assert EstadoEmAnalise().nome() == "Em Análise"
    assert EstadoFinalizada().nome() == "Finalizada"
    assert EstadoCancelada().nome() == "Cancelada"

#TESTES DE REGRAS DE NEGÓCIO E BLOQUEIOS

def test_bloqueio_de_cancelamento_pelo_aluno_em_analise():
    """Verifica se o erro correto é lançado quando o aluno tenta cancelar algo em análise."""
    solicitacao = MockSolicitacao()
    solicitacao.alterar_estado(EstadoEmAnalise())
    
    with pytest.raises(CancelamentoNaoPermitidoError) as excinfo:
        solicitacao.estado_atual.cancelar(solicitacao)
    
    #Verifica se a mensagem de erro identifica o estado atual
    assert "Em Análise" in str(excinfo.value)

#TESTES DE IMUTABILIDADE (ESTADOS TERMINAIS)

@pytest.mark.parametrize("estado_terminal", [EstadoFinalizada(), EstadoCancelada()])
def test_estados_terminais_devem_barrar_qualquer_acao(estado_terminal):
    """
    Testa a 'Imutabilidade Pós-Finalização'.
    Nenhuma ação (avançar ou cancelar) deve ser permitida em estados terminais.
    """
    solicitacao = MockSolicitacao()
    solicitacao.alterar_estado(estado_terminal)
    
    #Testar tentativa de Avançar
    with pytest.raises(TransicaoEstadoInvalidaError) as exc_avancar:
        estado_terminal.avancar(solicitacao)
    assert "avancar" in str(exc_avancar.value)
    
    #Testar tentativa de Cancelar
    with pytest.raises(TransicaoEstadoInvalidaError) as exc_cancelar:
        estado_terminal.cancelar(solicitacao)
    assert "cancelar" in str(exc_cancelar.value)

#TESTE DE ENCAPSULAMENTO

def test_metodo_executar_deve_ser_alias_de_avancar():
    """Garante que o método 'executar' ainda funciona (compatibilidade)."""
    solicitacao = MockSolicitacao()
    #Chama executar() que deve internamente chamar avancar()
    solicitacao.estado_atual.executar(solicitacao)
    
    assert isinstance(solicitacao.estado_atual, EstadoEmAnalise)