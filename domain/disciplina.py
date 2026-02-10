class Disciplina:
    
    def __init__(self, codigo: str, carga_horaria: int):
        self._codigo = codigo
        self._carga_horaria = carga_horaria

    @property
    def carga_horaria(self):
        return self._carga_horaria
    
    @property
    def codigo(self):
        return self._codigo