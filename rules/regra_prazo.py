from rules.regra_base import Regra
import datetime

class RegraPrazo(Regra):
    def validar(self, solicitacao):
        return getattr(solicitacao, "data", datetime.date.today()) <= getattr(solicitacao, "prazo", datetime.date.today())
