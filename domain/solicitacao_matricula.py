from domain.solicitacao import Solicitacao

class SolicitacaoMatricula(Solicitacao):
    """
    Representa o pedido de inclusão de um aluno em uma nova disciplina.
    """
    def __init__(self, aluno, disciplina):
        super().__init__(aluno)
        self._disciplina = disciplina
        """
        Inicializa o pedido de matrícula.
        
        :param aluno: Aluno interessado.
        :param disciplina: Disciplina pretendida.
        """

    def validar(self):
        return True
    """Verifica elegibilidade para matrícula."""
