# domain/disciplina.py
"""
Módulo que representa as unidades curriculares (disciplinas) da instituição.

Uma Disciplina é a unidade fundamental do currículo acadêmico. Além dos
atributos básicos (nome e carga horária), ela armazena seus pré-requisitos
(disciplinas que devem ser concluídas antes) e co-requisitos (disciplinas
que devem ser cursadas simultaneamente), informações essenciais para as
regras de validação de matrícula.
"""

from typing import List


class Disciplina:
    """
    Representa uma unidade curricular (matéria) oferecida pela instituição.

    Esta classe é central no modelo de domínio do SGSA, pois é referenciada
    por Curso (grade curricular), Historico (disciplinas cursadas), e pelas
    regras de validação de matrícula.

    Atributos públicos:
        nome (str): Nome oficial da disciplina (ex: "Cálculo I").
        carga_horaria (int): Total de horas-aula da disciplina.
        obrigatoria (bool): True se a disciplina é obrigatória no currículo;
                            False se é optativa ou complementar.

    Atributos privados:
        _pre_requisitos (list[Disciplina]): Disciplinas que o aluno deve ter
                         concluído com aprovação antes de se matricular aqui.
        _co_requisitos (list[Disciplina]): Disciplinas que devem ser cursadas
                        simultaneamente a esta (ex: teoria + laboratório).

    Princípios SOLID aplicados:
        - SRP: responsabilidade única de modelar uma disciplina curricular.
        - OCP: novos tipos de vínculo entre disciplinas podem ser adicionados
               sem alterar esta classe.

    Exemplo de uso:
        >>> calc1 = Disciplina("Cálculo I", 72)
        >>> calc2 = Disciplina("Cálculo II", 72)
        >>> calc2.adicionar_pre_requisito(calc1)
        >>> print(calc2.pre_requisitos)
        [Disciplina(nome='Cálculo I', carga_horaria=72)]
    """

    def __init__(self, nome: str, carga_horaria: int, obrigatoria: bool = True):
        """
        Inicializa uma nova disciplina com seus atributos principais.

        :param nome: Título oficial da disciplina conforme o catálogo
                     curricular (ex: "Programação Orientada a Objetos").
        :param carga_horaria: Valor inteiro representando o total de
                              horas-aula da disciplina (ex: 60, 72, 80).
        :param obrigatoria: Indica se a disciplina é obrigatória no
                            currículo. Padrão True. Disciplinas optativas
                            e de atividades complementares devem ser
                            criadas com obrigatoria=False.
        """
        self.nome = nome
        self.carga_horaria = carga_horaria
        self.obrigatoria = obrigatoria
        self._pre_requisitos: List["Disciplina"] = []
        self._co_requisitos: List["Disciplina"] = []

    # ------------------------------------------------------------------
    # Pré-requisitos
    # ------------------------------------------------------------------

    @property
    def pre_requisitos(self) -> List["Disciplina"]:
        """
        Retorna uma cópia da lista de disciplinas pré-requisito.

        Retorna uma cópia para proteger a lista interna de modificações
        externas diretas — o único caminho para adicionar pré-requisitos
        é via adicionar_pre_requisito().

        :return: Lista de objetos Disciplina que devem ser concluídos
                 antes da matrícula nesta disciplina.
        """
        return list(self._pre_requisitos)

    def adicionar_pre_requisito(self, disciplina: "Disciplina") -> None:
        """
        Registra uma disciplina como pré-requisito desta.

        Evita duplicatas: se a disciplina já estiver na lista,
        a operação é ignorada silenciosamente.

        :param disciplina: Objeto Disciplina que deve ser concluída
                           (com aprovação) antes desta.
        """
        if disciplina not in self._pre_requisitos:
            self._pre_requisitos.append(disciplina)

    # ------------------------------------------------------------------
    # Co-requisitos
    # ------------------------------------------------------------------

    @property
    def co_requisitos(self) -> List["Disciplina"]:
        """
        Retorna uma cópia da lista de disciplinas co-requisito.

        Co-requisitos são disciplinas que devem ser cursadas de forma
        simultânea (no mesmo semestre). Retorna cópia para proteger a
        lista interna.

        :return: Lista de objetos Disciplina de matrícula simultânea
                 obrigatória.
        """
        return list(self._co_requisitos)

    def adicionar_co_requisito(self, disciplina: "Disciplina") -> None:
        """
        Registra uma disciplina como co-requisito desta.

        Evita duplicatas: se a disciplina já estiver na lista,
        a operação é ignorada silenciosamente.

        :param disciplina: Objeto Disciplina que deve ser cursada
                           no mesmo semestre que esta.
        """
        if disciplina not in self._co_requisitos:
            self._co_requisitos.append(disciplina)

    # ------------------------------------------------------------------
    # Representação
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        """
        Retorna representação legível para exibição ao usuário.

        :return: String no formato 'Disciplina: Nome (XXh)'.
                 Ex: 'Disciplina: Cálculo I (72h)'.
        """
        return f"Disciplina: {self.nome} ({self.carga_horaria}h)"

    def __repr__(self) -> str:
        """
        Retorna representação técnica útil para depuração.

        :return: String com construtor equivalente.
                 Ex: "Disciplina(nome='Cálculo I', carga_horaria=72)".
        """
        return f"Disciplina(nome='{self.nome}', carga_horaria={self.carga_horaria})"

    def __eq__(self, other) -> bool:
        """
        Compara duas disciplinas pela igualdade de nome.

        Usado para verificar pertencimento em listas de pré/co-requisitos
        e no histórico do aluno.

        :param other: Outro objeto a comparar.
        :return: True se ambos são Disciplina com o mesmo nome.
        """
        if isinstance(other, Disciplina):
            return self.nome == other.nome
        return False

    def __hash__(self) -> int:
        """
        Permite uso de Disciplina como chave em dicionários e conjuntos.

        Necessário porque __eq__ foi sobrescrito; o hash é derivado
        do nome da disciplina.

        :return: Hash baseado no nome.
        """
        return hash(self.nome)
