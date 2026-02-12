# domain/disciplina.py
class Disciplina:
    def __init__(self, nome: str, carga_horaria: int):
        self.nome = nome
        self.carga_horaria = carga_horaria

    def __str__(self):
        return f"Disciplina: {self.nome} ({self.carga_horaria}h)"
