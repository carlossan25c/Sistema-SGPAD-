from domain.solicitacao_trancamento import SolicitacaoTrancamento
from domain.solicitacao_matricula import SolicitacaoMatricula
from domain.solicitacao_colacao import SolicitacaoColacao

class SolicitacaoService:
    """
    Serviço central que orquestra a criação e validação de solicitações.
    Implementa o padrão Factory para instanciar subtipos de Solicitação.
    """
    def criar_solicitacao(self, tipo, aluno, alvo):
        """
        Factory Method: Cria o objeto correto baseado na string de tipo.
        :param tipo: 'trancamento', 'matricula' ou 'colacao'.
        """
        if tipo == "trancamento":
            return SolicitacaoTrancamento(aluno, alvo)
        elif tipo == "matricula":
            return SolicitacaoMatricula(aluno, alvo)
        elif tipo == "colacao":
            return SolicitacaoColacao(aluno, alvo)
        else:
            raise ValueError("Tipo inválido.")

    def aplicar_regras(self, solicitacao, regras):
        """
        Aplica o padrão Strategy: valida uma série de regras acadêmicas.
        :param regras: Lista de objetos que implementam a interface Regra.
        :return: True se todas as regras forem satisfeitas.
        """
        return all(regra.validar(solicitacao) for regra in regras)
