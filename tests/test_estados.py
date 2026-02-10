import pytest
from domain.estado import EstadoAberta, EstadoEmAnalise, EstadoFinalizada

class MockSolicitacao:
    def __init__(self):
        self.estado_atual = EstadoAberta()

    def alterar_estado(self, novo_estado):
        self.estado_atual = novo_estado

def test_deve_avançar_de_aberta_para_em_analise():
    solicitacao = MockSolicitacao()
    estado_inicial = solicitacao.estado_atual
    
    estado_inicial.executar(solicitacao)
    
    #Verifica se a solicitação agora está em análise
    assert isinstance(solicitacao.estado_atual, EstadoEmAnalise)

def test_deve_avançar_de_em_analise_para_finalizada():
    solicitacao = MockSolicitacao()
    solicitacao.alterar_estado(EstadoEmAnalise())
    
    #Executa a lógica do estado "Em Análise"
    solicitacao.estado_atual.executar(solicitacao)
    
    #Verifica se a solicitação foi finalizada
    assert isinstance(solicitacao.estado_atual, EstadoFinalizada)

def test_estado_finalizada_nao_deve_alterar_mais_o_estado():
    solicitacao = MockSolicitacao()
    estado_final = EstadoFinalizada()
    solicitacao.alterar_estado(estado_final)
    
    
    estado_final.executar(solicitacao)
    
    #O estado deve continuar sendo Finalizada
    assert isinstance(solicitacao.estado_atual, EstadoFinalizada)