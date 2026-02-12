# domain/curso.py
class Curso:
    def __init__(self, nome: str):
        self.nome = nome
        self.disciplinas = []

    def __str__(self):
        return f"Curso: {self.nome}"
