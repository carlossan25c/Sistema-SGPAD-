import uuid


class IdentifiableMixin:
    """
    Mixin que fornece um identificador único universalmente exclusivo (UUID).

    Utilizado como herança múltipla para adicionar rastreabilidade por UUID
    a qualquer classe de domínio sem introduzir acoplamento conceitual.
    O MRO (Method Resolution Order) do Python garante que __init__ seja
    encadeado corretamente via super(), repassando *args e **kwargs.

    Padrão de uso:
        Deve ser listado ANTES da classe base na declaração de herança para
        que o MRO processe o Mixin antes da classe principal:
            class Aluno(IdentifiableMixin, Usuario): ...

    Exemplo de uso com herança múltipla:
        >>> class Aluno(IdentifiableMixin, Usuario):
        ...     def __init__(self, nome, email):
        ...         super().__init__(nome=nome, email=email)
        >>> a = Aluno("João", "joao@inst.edu.br")
        >>> print(a.id)  # UUID gerado automaticamente
    """

    def __init__(self, *args, **kwargs):
        """
        Gera o UUID e repassa os argumentos restantes pela cadeia MRO.

        :param args: Argumentos posicionais repassados ao próximo __init__.
        :param kwargs: Argumentos nomeados repassados ao próximo __init__.
        """
        self._id = str(uuid.uuid4())
        super().__init__(*args, **kwargs)

    @property
    def id(self) -> str:
        """
        Retorna o identificador UUID único do objeto (somente leitura).

        :return: String UUID no formato '8-4-4-4-12' (ex: 'a1b2c3d4-...').
        """
        return self._id
