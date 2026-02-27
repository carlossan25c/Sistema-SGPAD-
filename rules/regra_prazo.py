# rules/regra_prazo.py
"""
Módulo que implementa a regra de prazo do calendário acadêmico.

O trancamento de disciplina só é permitido dentro do período definido
pelo calendário acadêmico. Esta regra compara a data da solicitação com
o prazo limite registrado na própria solicitação.
"""

import datetime
from rules.regra_base import Regra
from domain.excecoes import ViolacaoRegraAcademicaError


class RegraPrazo(Regra):
    """
    Verifica se a solicitação foi realizada dentro do período permitido
    pelo calendário acadêmico.

    Compara solicitacao.data (quando foi feita) com solicitacao.prazo
    (último dia válido). Se a data for posterior ao prazo, a solicitação
    está fora do período e deve ser negada.

    Aplica-se a: SolicitacaoTrancamento (e qualquer outra que tenha
    atributos data e prazo).

    Atributos consultados da solicitação:
        solicitacao.data (datetime.date): data de criação da solicitação.
                          Fallback: datetime.date.today().
        solicitacao.prazo (datetime.date): prazo limite do calendário.
                          Fallback: datetime.date.today().

    Uso do getattr para robustez:
        Se a solicitação não possuir os atributos data ou prazo, usa
        datetime.date.today() como valor padrão, evitando AttributeError
        e assumindo que a solicitação está no prazo.

    Exemplo:
        >>> ontem = datetime.date.today() - datetime.timedelta(days=1)
        >>> sol = SolicitacaoTrancamento(aluno, disc,
        ...     data=datetime.date.today(),
        ...     prazo=ontem)
        >>> RegraPrazo().validar(sol)
        # Levanta: "Prazo acadêmico encerrado.
        #  Data da solicitação: DD/MM/AAAA, prazo limite: DD/MM/AAAA."
    """

    def validar(self, solicitacao) -> bool:
        """
        Verifica se a solicitação foi feita dentro do prazo acadêmico.

        :param solicitacao: Objeto Solicitacao com atributos data e prazo.
                            Se ausentes, assume datetime.date.today() para ambos.
        :raises ViolacaoRegraAcademicaError: se data > prazo, com as datas
                                             formatadas no formato DD/MM/AAAA.
        :return: True se data <= prazo.
        """
        hoje = datetime.date.today()
        data = getattr(solicitacao, "data", hoje)
        prazo = getattr(solicitacao, "prazo", hoje)

        if data > prazo:
            raise ViolacaoRegraAcademicaError(
                mensagem=(
                    f"Prazo acadêmico encerrado. "
                    f"Data da solicitação: {data.strftime('%d/%m/%Y')}, "
                    f"prazo limite: {prazo.strftime('%d/%m/%Y')}."
                ),
                regra="RegraPrazo"
            )
        return True
