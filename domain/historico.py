# domain/historico.py
"""
Módulo que representa o histórico acadêmico de um aluno.

O Historico é o registro oficial das disciplinas cursadas e das notas
obtidas pelo aluno ao longo do curso. Ele é a fonte de verdade consultada
pelas regras de validação para verificar aprovações, calcular créditos,
contar trancamentos e checar o status do vínculo.
"""

from typing import Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.disciplina import Disciplina


class Historico:
    """
    Armazena e gerencia o histórico acadêmico completo de um aluno.

    Esta classe é composta dentro de Aluno (composição) e é consultada
    intensamente pelas regras de validação (Strategy). Ela centraliza
    toda a informação sobre o desempenho acadêmico passado do aluno,
    tornando-se a única fonte necessária para qualquer verificação
    de elegibilidade.

    Atributos internos:
        _disciplinas (dict): Mapeamento de Disciplina → nota (float).
                             Representa todas as disciplinas já cursadas,
                             aprovadas ou não.
        _trancamentos (int): Contador de quantas vezes o aluno já
                             trancou o curso. Consultado por
                             RegraLimiteTrancamentos.
        _status_vinculo (str): Status atual do vínculo institucional
                               do aluno. Valores possíveis: 'Ativo',
                               'Trancado', 'Egresso'.

    Constante de classe:
        NOTA_MINIMA_APROVACAO (float): Nota mínima para aprovação.
                                       Padrão: 5.0.

    Exemplo de uso:
        >>> historico = Historico()
        >>> historico.adicionar_disciplina(calc1, nota=7.5)
        >>> historico.foi_aprovado(calc1)
        True
        >>> historico.total_creditos()
        72
    """

    NOTA_MINIMA_APROVACAO: float = 5.0

    def __init__(self):
        """
        Inicializa um histórico vazio com vínculo ativo e sem trancamentos.

        O histórico começa limpo: nenhuma disciplina registrada, zero
        trancamentos e status de vínculo 'Ativo', representando um aluno
        recém-ingressado na instituição.
        """
        self._disciplinas: Dict["Disciplina", float] = {}
        self._trancamentos: int = 0
        self._status_vinculo: str = "Ativo"

    # ------------------------------------------------------------------
    # Disciplinas e notas
    # ------------------------------------------------------------------

    def adicionar_disciplina(self, disciplina: "Disciplina", nota: float) -> None:
        """
        Registra uma disciplina cursada com a nota obtida pelo aluno.

        Se a disciplina já estiver no histórico, a nota é sobrescrita,
        permitindo o registro de situações como aproveitamento de estudos
        ou segunda chamada.

        :param disciplina: Objeto Disciplina que foi cursada.
        :param nota: Nota final obtida pelo aluno, no intervalo de 0.0
                     a 10.0. Notas abaixo de NOTA_MINIMA_APROVACAO
                     indicam reprovação.
        """
        self._disciplinas[disciplina] = nota

    def foi_aprovado(self, disciplina: "Disciplina") -> bool:
        """
        Verifica se o aluno foi aprovado em uma disciplina específica.

        Consulta o histórico e compara a nota obtida com a nota mínima
        de aprovação. Se a disciplina não constar no histórico (nunca
        cursada), retorna False.

        :param disciplina: Objeto Disciplina a ser verificado.
        :return: True se a nota for >= NOTA_MINIMA_APROVACAO;
                 False se reprovado ou se a disciplina não foi cursada.
        """
        nota = self._disciplinas.get(disciplina)
        if nota is None:
            return False
        return nota >= self.NOTA_MINIMA_APROVACAO

    def disciplinas_aprovadas(self) -> List["Disciplina"]:
        """
        Retorna a lista completa de disciplinas com aprovação.

        Utilizada principalmente pela RegraElegibilidade para verificar
        a integralização do currículo antes da colação de grau.

        :return: Lista de objetos Disciplina com nota >= NOTA_MINIMA_APROVACAO.
        """
        return [
            d for d, n in self._disciplinas.items()
            if n >= self.NOTA_MINIMA_APROVACAO
        ]

    def total_creditos(self) -> int:
        """
        Calcula a soma das cargas horárias de todas as disciplinas aprovadas.

        Representa o total de créditos (horas) acumulados pelo aluno ao
        longo do curso. É consultado por RegraCreditos e RegraElegibilidade.

        :return: Inteiro com o total de horas-crédito aprovadas.
                 Retorna 0 se nenhuma disciplina foi aprovada ainda.
        """
        return sum(
            d.carga_horaria
            for d, n in self._disciplinas.items()
            if n >= self.NOTA_MINIMA_APROVACAO
        )

    # ------------------------------------------------------------------
    # Trancamentos
    # ------------------------------------------------------------------

    @property
    def trancamentos(self) -> int:
        """
        Número de vezes que o aluno já trancou o curso.

        Consultado por RegraLimiteTrancamentos para verificar se o aluno
        ainda possui trancamentos disponíveis (limite padrão: 4).

        :return: Inteiro com o total de trancamentos realizados.
        """
        return self._trancamentos

    def registrar_trancamento(self) -> None:
        """
        Incrementa o contador de trancamentos de curso do aluno.

        Deve ser chamado toda vez que um trancamento de curso for
        efetivamente concedido e processado pelo setor acadêmico.
        """
        self._trancamentos += 1

    # ------------------------------------------------------------------
    # Status de vínculo
    # ------------------------------------------------------------------

    @property
    def status_vinculo(self) -> str:
        """
        Status atual do vínculo institucional do aluno.

        Consultado por RegraVinculoAtivo para impedir trancamentos
        de alunos já trancados ou egressos.

        Valores possíveis:
            - 'Ativo': aluno regularmente matriculado.
            - 'Trancado': aluno com curso trancado no período atual.
            - 'Egresso': aluno que concluiu ou foi desligado do curso.

        :return: String com o status do vínculo.
        """
        return self._status_vinculo

    @status_vinculo.setter
    def status_vinculo(self, novo_status: str) -> None:
        """
        Atualiza o status do vínculo do aluno.

        Realiza validação dos valores permitidos antes de atualizar,
        garantindo a integridade dos dados.

        :param novo_status: Novo status. Deve ser um dos valores:
                            'Ativo', 'Trancado' ou 'Egresso'.
        :raises ValueError: Se o valor informado não for um dos
                            status permitidos.
        """
        permitidos = {"Ativo", "Trancado", "Egresso"}
        if novo_status not in permitidos:
            raise ValueError(
                f"Status de vínculo inválido: '{novo_status}'. "
                f"Valores aceitos: {sorted(permitidos)}."
            )
        self._status_vinculo = novo_status
