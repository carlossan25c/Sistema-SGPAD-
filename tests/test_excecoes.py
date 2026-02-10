import pytest
from domain.solicitacao_matricula import SolicitacaoMatricula
from domain.solicitacao_colacao import SolicitacaoColacao
from rules.regra_creditos import RegraCreditos
from unittest.mock import MagicMock

# Violação de Regras de Fluxo (Estado)
def test_deve_lancar_erro_ao_reabrir_solicitacao_finalizada():
    """Garante que o sistema impeça a reabertura de solicitações encerradas."""
    solicitacao = SolicitacaoMatricula(aluno=None, disciplina=None)
    solicitacao.mudar_estado("Finalizada")
    
    
    with pytest.raises(ValueError, match="Não é possível reabrir solicitação finalizada."):
        solicitacao.mudar_estado("Aberta")

# Dados Inválidos ou Ausentes
def test_deve_lancar_erro_ao_criar_solicitacao_sem_aluno():
    """Verifica se o sistema impede a criação de pedidos sem um responsável."""
    # Teste de erro ao tentar instanciar sem argumentos obrigatórios
    with pytest.raises(TypeError):
        # Tentando criar sem passar o argumento 'aluno'
        solicitacao = SolicitacaoColacao() 

# Falha em Regras de Elegibilidade (Regra de Créditos)
def test_deve_lancar_excecao_quando_creditos_insuficientes():
    """Garante que a regra de créditos levante um erro se o aluno não atingir o mínimo."""
    # Criação da regra com o valor esperado de 200 créditos
    regra = RegraCreditos()
    
    # Criação de um mock de aluno com apenas 150 créditos
    aluno_mock = MagicMock()

    aluno_mock.historico.total_creditos.return_value = 150

    # Criação da disciplina mock com uma carga horária definida
    disciplina_mock = MagicMock()
    # Configuração para retornar 200 (ou qualquer valor > 150 para forçar o erro)
    disciplina_mock.carga_horaria = 200 

    # Criação do curso mock e da lista de disciplinas contendo essa disciplina
    curso_mock = MagicMock()
    curso_mock.disciplinas = [disciplina_mock]

    solicitacao = SolicitacaoColacao(aluno=aluno_mock, curso=curso_mock)
    
    with pytest.raises(ValueError, match="Créditos insuficientes para Colação de Grau"):
        if not regra.validar(solicitacao):
            raise ValueError("Créditos insuficientes para Colação de Grau")