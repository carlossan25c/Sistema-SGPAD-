from rules.regra_base import Regra
import datetime

class RegraPrazo(Regra):
    """
    Verifica se a solicitação foi realizada dentro do período permitido pelo calendário.
    """
    def validar(self, solicitacao):
        return getattr(solicitacao, "data", datetime.date.today()) <= getattr(solicitacao, "prazo", datetime.date.today())
    """
        Compara a data da solicitação com o prazo estipulado.
        Usa getattr para evitar erros caso os campos 'data' ou 'prazo' não existam.
        """
