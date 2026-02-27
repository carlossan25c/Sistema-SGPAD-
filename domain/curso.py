# domain/curso.py
"""
Módulo que representa um curso de graduação da instituição.

O Curso define o currículo acadêmico ao qual um aluno está vinculado.
Além de agrupar as disciplinas da grade curricular, ele armazena
parâmetros institucionais importantes para as regras de validação,
como o limite de carga horária semestral e o mínimo de horas optativas
exigidas para a colação de grau.
"""

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.disciplina import Disciplina


class Curso:
    """
    Representa um curso de graduação ou pós-graduação da instituição.

    O Curso é referenciado por Aluno (composição) e por SolicitacaoColacao.
    Seus atributos de configuração (limite semestral, mínimo de optativas)
    são consultados diretamente pelas regras de validação, eliminando a
    necessidade de valores hardcoded nas regras.

    Atributos públicos:
        nome (str): Nome oficial do curso (ex: "Ciência da Computação").
        limite_horas_semestrais (int): Máximo de horas que um aluno pode
                                       cursar em um único semestre.
                                       Padrão: 360h.
        min_horas_optativas (int): Mínimo de horas em disciplinas optativas
                                   ou complementares exigido para colação.
                                   Padrão: 0h (sem exigência).

    Atributo privado:
        _disciplinas (list[Disciplina]): Grade curricular completa do curso.

    Exemplo de uso:
        >>> curso = Curso("Engenharia de Software",
        ...               limite_horas_semestrais=400,
        ...               min_horas_optativas=120)
        >>> tcc = Disciplina("TCC", 80, obrigatoria=True)
        >>> curso.adicionar_disciplina(tcc)
        >>> curso.disciplinas_obrigatorias()
        [Disciplina(nome='TCC', carga_horaria=80)]
    """

    def __init__(self, nome: str,
                 limite_horas_semestrais: int = 360,
                 min_horas_optativas: int = 0):
        """
        Inicializa o curso com suas configurações institucionais.

        :param nome: Nome oficial do curso conforme registro na instituição.
        :param limite_horas_semestrais: Teto de carga horária permitido por
                                        semestre. Consultado por
                                        RegraLimiteCargaHoraria. Padrão: 360h.
        :param min_horas_optativas: Total mínimo de horas em disciplinas
                                    optativas/complementares para que o aluno
                                    possa colar grau. Consultado por
                                    RegraElegibilidade. Padrão: 0h.
        """
        self.nome = nome
        self.limite_horas_semestrais = limite_horas_semestrais
        self.min_horas_optativas = min_horas_optativas
        self._disciplinas: List["Disciplina"] = []

    @property
    def disciplinas(self) -> List["Disciplina"]:
        """
        Retorna uma cópia da lista completa de disciplinas do curso.

        Retorna cópia para proteger a lista interna de modificações
        externas — a única forma de adicionar disciplinas é via
        adicionar_disciplina().

        :return: Lista com todos os objetos Disciplina da grade curricular.
        """
        return list(self._disciplinas)

    def adicionar_disciplina(self, disciplina: "Disciplina") -> None:
        """
        Adiciona uma disciplina à grade curricular do curso.

        Evita duplicatas: se a disciplina já estiver na grade,
        a operação é ignorada silenciosamente.

        :param disciplina: Objeto Disciplina a ser vinculado ao curso.
        """
        if disciplina not in self._disciplinas:
            self._disciplinas.append(disciplina)

    def disciplinas_obrigatorias(self) -> List["Disciplina"]:
        """
        Retorna apenas as disciplinas marcadas como obrigatórias.

        Utilizada por RegraElegibilidade para verificar se o aluno
        completou 100% das obrigatórias antes de solicitar a colação.

        :return: Lista de Disciplinas com atributo obrigatoria=True.
        """
        return [d for d in self._disciplinas if d.obrigatoria]

    def __str__(self) -> str:
        """
        Retorna representação legível do curso.

        :return: String no formato 'Curso: Nome'.
                 Ex: 'Curso: Ciência da Computação'.
        """
        return f"Curso: {self.nome}"
