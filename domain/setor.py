class SetorAcademico:
    def __init__(self, nome: str, responsavel: str):
        self._nome = nome
        self._responsavel = responsavel

    @property
    def nome(self):
        return self._nome
