# domain/setor.py
"""
Módulo que representa os setores administrativos da instituição.

Os setores acadêmicos são as unidades responsáveis por receber,
analisar e dar parecer sobre as solicitações dos alunos. Exemplos
reais incluem o DERCA (Departamento de Registro e Controle Acadêmico)
e as Coordenações de Curso.
"""


class SetorAcademico:
    """
    Representa um departamento ou unidade administrativa responsável
    por analisar solicitações acadêmicas dos alunos.

    No contexto do padrão Observer, o SetorAcademico é um dos
    destinatários das notificações disparadas automaticamente quando
    uma nova solicitação é criada ou tem seu estado alterado.

    Atributos privados:
        _nome (str): Nome oficial do setor
                     (ex: 'Coordenação de Sistemas de Informação').
        _responsavel (str): Nome ou cargo do responsável pelo setor
                            (ex: 'Prof. Dr. João Mendes').

    Exemplo de uso:
        >>> setor = SetorAcademico("DERCA", "Coordenador de Registros")
        >>> print(setor.nome)
        DERCA
    """

    def __init__(self, nome: str, responsavel: str):
        """
        Inicializa o setor com nome e responsável.

        :param nome: Nome oficial do setor acadêmico
                     (ex: 'DERCA', 'Coordenação do Curso de ADS').
        :param responsavel: Nome ou título do responsável pelo setor,
                            que receberá as notificações de solicitações.
        """
        self._nome = nome
        self._responsavel = responsavel

    @property
    def nome(self) -> str:
        """
        Retorna o nome oficial do setor (somente leitura).

        :return: String com o nome do setor.
        """
        return self._nome

    @property
    def responsavel(self) -> str:
        """
        Retorna o nome ou cargo do responsável pelo setor (somente leitura).

        :return: String com o nome/cargo do responsável.
        """
        return self._responsavel
