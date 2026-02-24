from rules.regra_base import Regra

class RegraCreditos(Regra):
    """
    Valida se o aluno possui créditos suficientes no histórico para a solicitação.
    """
    def validar(self, solicitacao):
        return solicitacao.aluno.historico.total_creditos() >= solicitacao._curso.disciplinas[0].carga_horaria
    """
        Compara o total de créditos do aluno com a carga horária da primeira disciplina do curso.
        """
