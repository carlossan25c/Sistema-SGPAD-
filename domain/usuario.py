from abc import ABC

class Usuario(ABC):
    """
    Classe base abstrata que define a estrutura comum para todos os usuários do sistema.
    Não pode ser instanciada diretamente.
    """
    def __init__(self, nome: str, email: str):
        self._nome = nome
        self._email = email
        """
        Inicializa os dados básicos de um usuário.
        
        :param nome: Nome completo do usuário.
        :param email: Endereço de e-mail eletrônico.
        """

    @property
    def nome(self):
        return self._nome
    """Retorna o nome do usuário."""

    @property
    def email(self):
        return self._email
    """Retorna o e-mail do usuário."""
