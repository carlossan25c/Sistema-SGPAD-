from domain.solicitacao import Solicitacao

class SolicitacaoTrancamento(Solicitacao):
    """
    Especialização de Solicitação para pedidos de interrupção temporária (trancamento) 
    de uma disciplina específica.
    """
    def __init__(self, aluno, disciplina):
        super().__init__(aluno)
        self._disciplina = disciplina
        """
        Cria um pedido de trancamento.
        
        :param aluno: Aluno solicitante.
        :param disciplina: Disciplina a ser trancada.
        """

    def validar(self):
        return True  # lógica simplificada
    """
        Executa a validação lógica para o trancamento.
        :return: bool.
        """
