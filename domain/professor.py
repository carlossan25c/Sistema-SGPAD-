from domain.usuario import Usuario

class Professor(Usuario):
    """
    Especialização da classe Usuario para docentes da instituição.
    
    Atributos:
        _siape (str): Matrícula SIAPE do professor (identificador funcional).
        _disciplinas (list): Lista de disciplinas que o professor ministra.
    """
    def __init__(self, nome: str, email: str, siape: str):
        """
        Cria um objeto Professor herdando dados básicos de Usuario.
        
        :param nome: Nome completo do docente.
        :param email: Endereço de e-mail institucional.
        :param siape: Código identificador SIAPE.
        """
        super().__init__(nome, email)
        self._siape = siape
        self._disciplinas = []

    def adicionar_disciplina(self, disciplina):
        self._disciplinas.append(disciplina)
        """
        Vincula uma disciplina à grade de aulas do professor.
        
        :param disciplina: Objeto da classe Disciplina.
        """
