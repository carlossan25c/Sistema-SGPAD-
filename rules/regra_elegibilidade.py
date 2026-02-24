from rules.regra_base import Regra

class RegraElegibilidade(Regra):
    """
    Regra geral que verifica se o aluno atingiu um patamar mínimo de créditos (ex: 80h).
    """
    def validar(self, solicitacao):
        return solicitacao.aluno.historico.total_creditos() >= 80
    """Retorna True se o aluno tem 80 ou mais créditos."""
