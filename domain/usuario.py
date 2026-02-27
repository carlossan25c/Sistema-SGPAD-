# domain/usuario.py
"""
Módulo que define a classe base abstrata para todos os usuários do sistema.

Todo ator que interage com o SGSA — seja um aluno realizando solicitações
ou um professor vinculado a disciplinas — compartilha um conjunto mínimo
de atributos definidos aqui. A abstração impede a instanciação direta
de Usuario, forçando o uso das subclasses concretas (Aluno, Professor).
"""

from abc import ABC


class Usuario(ABC):
    """
    Classe base abstrata que define a estrutura comum para todos os
    usuários do sistema SGSA.

    Esta classe implementa o princípio da abstração da POO: ela define
    o contrato mínimo (nome e e-mail) que qualquer tipo de usuário deve
    possuir, sem permitir que seja instanciada diretamente.

    Herança:
        Subclasses concretas: Aluno, Professor.

    Princípios SOLID aplicados:
        - SRP: responsabilidade única de representar dados básicos de usuário.
        - OCP: novas categorias de usuário (ex: Coordenador) podem ser
               adicionadas estendendo esta classe sem modificá-la.
        - LSP: todas as subclasses respeitam o contrato definido aqui.

    Atributos (protegidos):
        _nome (str): Nome completo do usuário.
        _email (str): Endereço de e-mail institucional do usuário.

    Exemplo de uso (via subclasse):
        >>> aluno = Aluno("João Silva", "joao@inst.edu.br", "2023001", curso)
        >>> print(aluno.nome)   # acesso via property herdada
        João Silva
    """

    def __init__(self, nome: str, email: str):
        """
        Inicializa os dados básicos compartilhados por todos os usuários.

        Os atributos são protegidos (prefixo _) para que subclasses possam
        acessá-los diretamente, enquanto código externo deve usar as
        properties públicas.

        :param nome: Nome completo do usuário (ex: "Maria Oliveira").
        :param email: Endereço de e-mail institucional
                      (ex: "maria@universidade.edu.br").
        """
        self._nome = nome
        self._email = email

    @property
    def nome(self) -> str:
        """
        Retorna o nome completo do usuário.

        Property de leitura que encapsula o atributo protegido _nome,
        impedindo modificação direta após a criação do objeto.

        :return: String com o nome completo do usuário.
        """
        return self._nome

    @property
    def email(self) -> str:
        """
        Retorna o endereço de e-mail do usuário.

        Property de leitura que encapsula o atributo protegido _email.

        :return: String com o e-mail do usuário.
        """
        return self._email
