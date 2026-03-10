import pytest
from unittest.mock import MagicMock
from rules.regra_elegibilidade import RegraElegibilidade, MINIMO_CREDITOS_FALLBACK
from domain.excecoes import ViolacaoRegraAcademicaError

@pytest.fixture
def setup_solicitacao():
    """Prepara a estrutura de mocks para a solicitação."""
    solicitacao = MagicMock()
    # Dados básicos do curso
    solicitacao.aluno.curso.nome = "Medicina UFCA"
    solicitacao.aluno.curso.min_horas_optativas = 0
    solicitacao.aluno.curso.disciplinas_obrigatorias.return_value = []
    
    # Dados básicos do histórico
    solicitacao.aluno.historico.total_creditos.return_value = 0
    solicitacao.aluno.historico.disciplinas_aprovadas.return_value = []
    solicitacao.aluno.historico.foi_aprovado.return_value = False
    
    return solicitacao

#TESTES DE FALLBACK (Curso Vazio)

def test_fallback_deve_reprovar_se_creditos_abaixo_do_minimo(setup_solicitacao):
    regra = RegraElegibilidade()
    solicitacao = setup_solicitacao
    
    # Simula curso vazio e aluno com horas insuficientes
    solicitacao.aluno.historico.total_creditos.return_value = 100
    
    with pytest.raises(ViolacaoRegraAcademicaError) as excinfo:
        regra.validar(solicitacao)
    
    # Verifica se a mensagem contém os termos exatos do seu código
    assert "Integralização não verificável" in str(excinfo.value)
    assert f"Exigido ao menos {MINIMO_CREDITOS_FALLBACK}h" in str(excinfo.value)

#TESTES DE OBRIGATÓRIAS

def test_deve_reprovar_se_faltar_disciplina_obrigatoria(setup_solicitacao):
    regra = RegraElegibilidade()
    solicitacao = setup_solicitacao
    
    d1 = MagicMock(nome="Anatomia I")
    solicitacao.aluno.curso.disciplinas_obrigatorias.return_value = [d1]
    solicitacao.aluno.historico.foi_aprovado.return_value = False
    
    with pytest.raises(ViolacaoRegraAcademicaError) as excinfo:
        regra.validar(solicitacao)
    
    assert "Anatomia I" in str(excinfo.value)
    assert "pendente" in str(excinfo.value)

#TESTES DE OPTATIVAS

def test_deve_reprovar_se_horas_optativas_forem_insuficientes(setup_solicitacao):
    regra = RegraElegibilidade()
    solicitacao = setup_solicitacao
    
    # Configura curso com exigência de 100h
    solicitacao.aluno.curso.min_horas_optativas = 100
    solicitacao.aluno.curso.disciplinas_obrigatorias.return_value = []
    
    # Aluno tem apenas 60h em optativas
    opt = MagicMock(carga_horaria=60, obrigatoria=False)
    solicitacao.aluno.historico.disciplinas_aprovadas.return_value = [opt]
    
    with pytest.raises(ViolacaoRegraAcademicaError) as excinfo:
        regra.validar(solicitacao)
    
    # Mensagem sincronizada com o código
    assert "Carga horária de optativas insuficiente" in str(excinfo.value)
    assert "concluído: 60h" in str(excinfo.value)

# --- 4. CAMINHO FELIZ (Aprovação) ---

def test_deve_aprovar_aluno_apto(setup_solicitacao):
    regra = RegraElegibilidade()
    solicitacao = setup_solicitacao
    
    # Simula aluno que passou em tudo
    d_obrig = MagicMock(nome="Saúde Coletiva")
    solicitacao.aluno.curso.disciplinas_obrigatorias.return_value = [d_obrig]
    solicitacao.aluno.historico.foi_aprovado.return_value = True
    
    assert regra.validar(solicitacao) is True