from domain.solicitacao import Solicitacao

class SolicitacaoColacao(Solicitacao):
    """
    Representa um pedido formal de colação de grau (formatura) realizado por um aluno.
    Esta classe estende a funcionalidade básica de 'Solicitacao' para o contexto de conclusão de curso.
    """
    def __init__(self, aluno, curso):
        super().__init__(aluno)
        self._curso = curso
        """
        Inicializa uma solicitação de colação de grau.
        
        :param aluno: Instância da classe Aluno que está a requerer a formatura.
        :param curso: Instância da classe Curso na qual o aluno deseja graduar-se.
        """

    def validar(self):
        return True
    """
        Verifica se o aluno cumpre os requisitos para colar grau.
        
        Nota: Na implementação atual, retorna sempre True por padrão, mas deve ser 
        expandida para integrar com a lógica de regras (Strategy) do sistema.
        
        :return: bool (True se elegível).
        """
