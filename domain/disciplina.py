# domain/disciplina.py
class Disciplina:
    """
    Representa uma unidade curricular (matéria) oferecida pela instituição.
    
    Atributos:
        nome (str): Nome da disciplina.
        carga_horaria (int): Carga horária total da disciplina em horas.
    """
    def __init__(self, nome: str, carga_horaria: int):
        """
        Inicializa uma nova disciplina.
        
        :param nome: Título da matéria.
        :param carga_horaria: Valor inteiro representando as horas totais.
        """
        self.nome = nome
        self.carga_horaria = carga_horaria

    def __str__(self):
        """Retorna o nome e a carga horária formatados para exibição."""
        return f"Disciplina: {self.nome} ({self.carga_horaria}h)"
