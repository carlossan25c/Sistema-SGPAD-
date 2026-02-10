from domain.solicitacao_trancamento import SolicitacaoTrancamento
from domain.solicitacao_matricula import SolicitacaoMatricula
from domain.solicitacao_colacao import SolicitacaoColacao

class SolicitacaoService:
    def criar_solicitacao(self, tipo, aluno, alvo):
        if tipo == "trancamento":
            return SolicitacaoTrancamento(aluno, alvo)
        elif tipo == "matricula":
            return SolicitacaoMatricula(aluno, alvo)
        elif tipo == "colacao":
            return SolicitacaoColacao(aluno, alvo)
        else:
            raise ValueError("Tipo inválido.")

    def aplicar_regras(self, solicitacao, regras):
        return all(regra.validar(solicitacao) for regra in regras)
