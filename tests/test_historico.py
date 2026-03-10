import pytest
from domain.historico import Historico
from domain.disciplina import Disciplina

# --- FIXTURES ---

@pytest.fixture
def historico():
    """Cria um histórico limpo para os testes."""
    return Historico()

@pytest.fixture
def anatomia():
    return Disciplina(nome="Anatomia I", carga_horaria=80, obrigatoria=True)

@pytest.fixture
def fisiologia():
    return Disciplina(nome="Fisiologia", carga_horaria=60, obrigatoria=True)

#TESTES DE APROVAÇÃO E CRÉDITOS

def test_deve_identificar_aprovacao_corretamente(historico, anatomia):
    """Garante que a nota mínima (5.0) seja respeitada."""
    # Caso 1: Aprovado com nota exata (5.0)
    historico.adicionar_disciplina(anatomia, nota=5.0)
    assert historico.foi_aprovado(anatomia) is True
    
    # Caso 2: Reprovado com nota 4.9
    historico.adicionar_disciplina(anatomia, nota=4.9)
    assert historico.foi_aprovado(anatomia) is False

def test_calculo_total_de_creditos_apenas_aprovadas(historico, anatomia, fisiologia):
    """Verifica se o total de créditos ignora disciplinas reprovadas."""
    historico.adicionar_disciplina(anatomia, nota=7.0)  # 80h
    historico.adicionar_disciplina(fisiologia, nota=3.0) # 60h (reprovado)
    
    # O total deve ser apenas as 80h de Anatomia
    assert historico.total_creditos() == 80
    assert len(historico.disciplinas_aprovadas()) == 1

def test_disciplina_nao_cursada_deve_retornar_reprovado(historico, anatomia):
    """Garante que consultar uma disciplina que não está no histórico não gere erro."""
    assert historico.foi_aprovado(anatomia) is False

#TESTES DE TRANCAMENTO

def test_registro_e_contador_de_trancamentos(historico):
    """Valida o contador usado pela RegraLimiteTrancamentos."""
    assert historico.trancamentos == 0
    historico.registrar_trancamento()
    historico.registrar_trancamento()
    assert historico.trancamentos == 2

#TESTES DE STATUS DE VÍNCULO

def test_alteracao_de_status_valido(historico):
    """Testa a transição de vínculo institucional."""
    historico.status_vinculo = "Trancado"
    assert historico.status_vinculo == "Trancado"
    
    historico.status_vinculo = "Egresso"
    assert historico.status_vinculo == "Egresso"

def test_impedir_status_de_vinculo_invalido(historico):
    """Garante que o sistema não aceite estados de vínculo inexistentes."""
    with pytest.raises(ValueError) as excinfo:
        historico.status_vinculo = "Desistente" # Não está no set permitido
    
    assert "Status de vínculo inválido" in str(excinfo.value)
    assert "Ativo" in str(excinfo.value) # Verifica se a mensagem sugere os corretos

#TESTE DE SOBRESCRITA DE NOTA

def test_sobrescrever_nota_da_mesma_disciplina(historico, anatomia):
    """Testa o cenário de re-cursar ou correção de nota."""
    historico.adicionar_disciplina(anatomia, nota=2.0)
    assert historico.total_creditos() == 0
    
    # Aluno faz segunda chamada ou re-cursa e passa
    historico.adicionar_disciplina(anatomia, nota=6.0)
    assert historico.total_creditos() == 80