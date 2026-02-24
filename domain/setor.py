class SetorAcademico:
    """
    Define os departamentos ou unidades administrativas responsáveis por analisar solicitações.
    """
    def __init__(self, nome: str, responsavel: str):
        self._nome = nome
        self._responsavel = responsavel
        """
        Inicializa um setor acadêmico.
        
        :param nome: Nome do setor (ex: DERCA, Coordenação de Curso).
        :param responsavel: Nome da pessoa ou cargo responsável pelo setor.
        """

    @property
    def nome(self):
        return self._nome
    """Getter para o nome do setor."""
