# domain/professor.py
"""
Módulo que representa o docente da instituição.

O Professor é um tipo especializado de Usuario que pode ser vinculado
a disciplinas da grade curricular. No contexto atual do SGSA ele serve
como ator de referência no domínio, podendo futuramente ser integrado
como responsável por aprovar solicitações de matrícula ou trancamento.
"""

from domain.usuario import Usuario


class Professor(Usuario):
    """
    Especialização da classe Usuario para os docentes da instituição.

    Herda os atributos básicos de Usuario (nome, e-mail) e acrescenta
    o identificador funcional SIAPE e a lista de disciplinas ministradas.

    Herança:
        Usuario (ABC) → Professor (concreto).

    Atributos herdados:
        nome (str): Nome completo do professor (via property de Usuario).
        email (str): E-mail institucional (via property de Usuario).

    Atributos próprios:
        _siape (str): Código SIAPE — identificador funcional único de
                      servidores públicos federais da educação.
        _disciplinas (list): Disciplinas atualmente ministradas.

    Exemplo de uso:
        >>> prof = Professor("Dr. Carlos Maia", "carlos@inst.edu.br", "1234567")
        >>> prof.adicionar_disciplina(disciplina_poo)
        >>> print(prof.disciplinas)
        [Disciplina(nome='POO', carga_horaria=60)]
    """

    def __init__(self, nome: str, email: str, siape: str):
        """
        Inicializa o professor com dados pessoais e matrícula SIAPE.

        :param nome: Nome completo do docente
                     (ex: "Dr. Rafael Souza").
        :param email: E-mail institucional do professor
                      (ex: "rafael@universidade.edu.br").
        :param siape: Número SIAPE — identificador funcional único
                      para servidores do ensino público federal
                      (ex: "1234567").
        """
        super().__init__(nome, email)
        self._siape = siape
        self._disciplinas = []

    @property
    def siape(self) -> str:
        """
        Retorna o código SIAPE do professor (somente leitura).

        :return: String com o número SIAPE.
        """
        return self._siape

    @property
    def disciplinas(self) -> list:
        """
        Retorna uma cópia da lista de disciplinas ministradas.

        Retorna cópia para proteger a lista interna de modificações
        externas.

        :return: Lista de objetos Disciplina vinculados ao professor.
        """
        return list(self._disciplinas)

    def adicionar_disciplina(self, disciplina) -> None:
        """
        Vincula uma disciplina à carga de aulas do professor.

        Permite construir a relação entre o docente e as matérias que
        ministra, útil para notificações e relatórios futuros.

        :param disciplina: Objeto Disciplina a ser vinculado.
        """
        self._disciplinas.append(disciplina)
