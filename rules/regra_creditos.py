from rules.regra_base import Regra

class RegraCreditos(Regra):
    def validar(self, solicitacao):
        return solicitacao.aluno.historico.total_creditos() >= solicitacao._curso.disciplinas[0].carga_horaria
