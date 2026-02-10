from rules.regra_base import Regra

class RegraElegibilidade(Regra):
    def validar(self, solicitacao):
        return solicitacao.aluno.historico.total_creditos() >= 80
