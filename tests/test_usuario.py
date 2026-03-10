import pytest
from domain.usuario import Usuario

#MOCK CONCRETO PARA TESTAR HERANÇA

class UsuarioConcreto(Usuario):
    """Subclasse apenas para validar que a herança funciona como esperado."""
    pass

#TESTE DE INSTANCIAÇÃO

def test_instanciacao_usuario_base():
    """
    Valida que a classe base armazena os dados corretamente.
    """
    user = Usuario("Nome Teste", "teste@ufca.edu.br")
    assert user.nome == "Nome Teste"
    assert user.email == "teste@ufca.edu.br"

#TESTE DE PROPRIEDADES E ENCAPSULAMENTO

def test_usuario_concreto_deve_retornar_dados_via_properties():
    """Valida se as properties nome e email funcionam em subclasses."""
    user = UsuarioConcreto("Maria Oliveira", "maria@ufca.edu.br")
    
    assert user.nome == "Maria Oliveira"
    assert user.email == "maria@ufca.edu.br"

def test_nome_e_email_devem_ser_somente_leitura():
    """Verifica se o encapsulamento impede a alteração direta dos dados."""
    user = UsuarioConcreto("Maria Oliveira", "maria@ufca.edu.br")
    
    # Tentativas de alteração devem levantar AttributeError
    with pytest.raises(AttributeError):
        user.nome = "Novo Nome"
        
    with pytest.raises(AttributeError):
        user.email = "novo@email.com"

#TESTE DE ATRIBUTOS PROTEGIDOS

def test_acesso_aos_atributos_protegidos():
    """Garante que o prefixo '_' está sendo usado internamente."""
    user = UsuarioConcreto("Teste", "teste@ufca.edu.br")
    # Acessando os atributos protegidos diretamente (permitido em testes/subclasses)
    assert user._nome == "Teste"
    assert user._email == "teste@ufca.edu.br"