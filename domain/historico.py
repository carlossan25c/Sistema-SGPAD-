class Historico:
    def __init__(self):
        self._disciplinas = {}
    
    def adicionar_disciplina(self, disciplina, nota: float):
        self._disciplinas[disciplina] = nota

    def total_creditos(self):
        return sum(d.carga_horaria for d in self._disciplinas.keys())
