class Historico:
    def __init__(self):
        self._disciplinas = {}
        """
    Armazena o registro de disciplinas cursadas e notas obtidas pelo aluno.
    """
    
    def adicionar_disciplina(self, disciplina, nota: float):
        self._disciplinas[disciplina] = nota
        """Vincula uma disciplina concluída ao histórico do aluno."""

    def total_creditos(self):
        return sum(d.carga_horaria for d in self._disciplinas.keys())
    """Calcula a soma da carga horária de todas as disciplinas no histórico."""
