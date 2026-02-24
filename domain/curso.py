# domain/curso.py
class Curso:
    """
    Representa uma graduação ou curso dentro da instituição.
    
    Atributos:
        nome (str): O nome oficial do curso.
        disciplinas (list): Lista de objetos da classe Disciplina vinculados ao curso.
    """
    def __init__(self, nome: str):
        """
        Inicializa uma nova instância de Curso.
        
        :param nome: Nome descritivo do curso.
        """
        self.nome = nome
        self.disciplinas = []

    def __str__(self):
        return f"Curso: {self.nome}"
    """Retorna a representação textual do curso."""
