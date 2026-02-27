# domain/aluno.py
"""
Módulo que representa o estudante no sistema SGSA.

O Aluno é o ator central do sistema: é ele quem realiza as solicitações
acadêmicas (matrícula, trancamento, colação). Esta classe agrega todos
os dados necessários para as validações: curso, histórico acadêmico
e pendências documentais.
"""

from domain.curso import Curso
from domain.historico import Historico


class Aluno:
    """
    Representa um estudante matriculado na instituição.

    Esta classe agrega (composição) as classes Curso e Historico, tornando-se
    a fonte principal de dados consultada pelas regras de validação. Toda
    informação necessária para decidir se uma solicitação pode ser aprovada
    está acessível a partir do objeto Aluno.

    Encapsulamento:
        - matricula e curso são atributos privados (name mangling __) com
          acesso controlado por properties, evitando modificações acidentais.
        - pendencias é protegida com métodos dedicados para adicionar e remover.

    Atributos públicos:
        nome (str): Nome completo do aluno.
        email (str): E-mail institucional do aluno.
        historico (Historico): Histórico acadêmico completo (composição).

    Atributos privados:
        __matricula (str): Código de matrícula único do aluno.
        __curso (Curso): Curso ao qual o aluno está vinculado.
        _pendencias (list[str]): Pendências documentais ou de biblioteca
                                  que bloqueiam a colação de grau.

    Exemplo de uso:
        >>> curso = Curso("Sistemas de Informação")
        >>> aluno = Aluno("Ana Lima", "ana@inst.edu.br", "2022001", curso)
        >>> aluno.adicionar_pendencia("Débito na biblioteca")
        >>> aluno.tem_pendencias()
        True
    """

    def __init__(self, nome: str, email: str, matricula: str, curso: Curso):
        """
        Inicializa um aluno com seus dados cadastrais e vínculo institucional.

        :param nome: Nome completo do estudante.
        :param email: Endereço de e-mail institucional.
        :param matricula: Código de matrícula único do aluno no sistema
                          acadêmico (ex: '2023001').
        :param curso: Objeto Curso ao qual o aluno está vinculado.
                      Deve ser uma instância válida da classe Curso.
        """
        self.nome = nome
        self.email = email
        self.__matricula = matricula
        self.__curso = curso
        self.historico = Historico()
        self._pendencias: list = []

    # ------------------------------------------------------------------
    # Matrícula
    # ------------------------------------------------------------------

    @property
    def matricula(self) -> str:
        """
        Retorna o código de matrícula do aluno (somente leitura).

        A matrícula não pode ser alterada após a criação do objeto,
        pois é o identificador único e imutável do aluno no sistema.

        :return: String com o código de matrícula.
        """
        return self.__matricula

    # ------------------------------------------------------------------
    # Curso
    # ------------------------------------------------------------------

    @property
    def curso(self) -> Curso:
        """
        Retorna o objeto Curso ao qual o aluno está vinculado.

        :return: Instância de Curso associada ao aluno.
        """
        return self.__curso

    @curso.setter
    def curso(self, value: Curso) -> None:
        """
        Atualiza o curso do aluno com validação de tipo.

        Garante que apenas objetos da classe Curso sejam atribuídos,
        protegendo a integridade do domínio (ex: evita atribuir uma
        string ou None acidentalmente).

        :param value: Novo objeto Curso a ser vinculado ao aluno.
        :raises TypeError: Se value não for uma instância de Curso.
        """
        if not isinstance(value, Curso):
            raise TypeError(
                f"Curso deve ser um objeto da classe Curso, "
                f"mas foi recebido: {type(value).__name__}."
            )
        self.__curso = value

    # ------------------------------------------------------------------
    # Pendências documentais
    # ------------------------------------------------------------------

    @property
    def pendencias(self) -> list:
        """
        Retorna uma cópia da lista de pendências documentais do aluno.

        Pendências são situações que impedem a colação de grau, como
        débitos na biblioteca ou documentos de registro civil pendentes.
        Retorna cópia para proteger a lista interna.

        :return: Lista de strings descrevendo cada pendência.
        """
        return list(self._pendencias)

    def adicionar_pendencia(self, descricao: str) -> None:
        """
        Registra uma nova pendência que impede a colação de grau.

        Consultado por RegraPendenciaDocumentacao. Exemplos de pendências:
        'Débito na biblioteca', 'Certidão de nascimento pendente'.

        :param descricao: Descrição legível da pendência a ser registrada.
        """
        self._pendencias.append(descricao)

    def remover_pendencia(self, descricao: str) -> None:
        """
        Remove uma pendência já resolvida pelo aluno.

        Se a pendência não existir na lista, a operação é ignorada
        silenciosamente.

        :param descricao: Descrição exata da pendência a ser removida
                          (deve coincidir com o valor registrado).
        """
        if descricao in self._pendencias:
            self._pendencias.remove(descricao)

    def tem_pendencias(self) -> bool:
        """
        Verifica se o aluno possui alguma pendência aberta.

        Consultado por RegraPendenciaDocumentacao antes de permitir
        a criação de uma SolicitacaoColacao.

        :return: True se houver ao menos uma pendência; False caso contrário.
        """
        return len(self._pendencias) > 0

    # ------------------------------------------------------------------
    # Representação
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        """
        Retorna representação legível do aluno para exibição.

        :return: String no formato 'Aluno: Nome (Matrícula) - Curso: NomeCurso'.
                 Ex: 'Aluno: Ana Lima (2022001) - Curso: Sistemas de Informação'.
        """
        return f"Aluno: {self.nome} ({self.matricula}) - Curso: {self.curso.nome}"
