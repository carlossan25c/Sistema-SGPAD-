# infrastructure/repositorio_disciplina.py
"""
Módulo que implementa o repositório de persistência de disciplinas.

Gerencia as operações de leitura e escrita de disciplinas no arquivo JSON,
seguindo o mesmo padrão Repository utilizado pelos demais repositórios
do sistema.
"""

from infrastructure.db_config import load_db, save_db


class RepositorioDisciplina:
    """
    Gerencia a persistência de objetos Disciplina no arquivo JSON.

    Responsável por salvar e recuperar os dados básicos das disciplinas
    (nome e carga horária) no arquivo sgsa.json. Relações como
    pré-requisitos e co-requisitos não são persistidas nesta versão —
    elas são configuradas em memória ao inicializar o sistema.

    Padrão aplicado: Repository.

    Princípios SOLID:
        - SRP: responsabilidade única de persistir e recuperar disciplinas.

    Nota de escopo:
        Esta implementação não persiste os atributos pre_requisitos,
        co_requisitos e obrigatoria, que são relações entre objetos.
        Em uma versão futura, esses vínculos poderiam ser armazenados
        como listas de nomes ou IDs no JSON.

    Exemplo de uso:
        >>> repo = RepositorioDisciplina()
        >>> repo.adicionar(Disciplina("Cálculo I", 72))
        >>> for d in repo.listar():
        ...     print(d)  # ('Cálculo I', 72)
    """

    def adicionar(self, disciplina) -> None:
        """
        Persiste uma nova disciplina no arquivo JSON.

        Salva apenas os campos primitivos da disciplina (nome e
        carga_horaria), que são suficientes para a persistência básica.

        :param disciplina: Objeto Disciplina a ser persistido.
        """
        db = load_db()
        db['disciplinas'].append({
            "nome": disciplina.nome,
            "carga_horaria": disciplina.carga_horaria
        })
        save_db(db)

    def listar(self) -> list:
        """
        Retorna todas as disciplinas cadastradas como lista de tuplas.

        Cada tupla contém: (nome, carga_horaria).

        :return: Lista de tuplas (nome, carga_horaria).
                 Retorna lista vazia se não houver disciplinas cadastradas.
        """
        db = load_db()
        return [
            (d['nome'], d['carga_horaria'])
            for d in db['disciplinas']
        ]
