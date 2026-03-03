# infrastructure/repositorio_disciplina.py
"""
Módulo que implementa o repositório de persistência de disciplinas.

Gerencia as operações de leitura e escrita de disciplinas no arquivo JSON,
seguindo o mesmo padrão Repository utilizado pelos demais repositórios
do sistema.

Nesta versão, os atributos pre_requisitos, co_requisitos e obrigatoria
também são persistidos, permitindo que as regras de validação funcionem
corretamente ao reconstruir as disciplinas a partir do banco de dados.
"""

from infrastructure.db_config import load_db, save_db


class RepositorioDisciplina:
    """
    Gerencia a persistência de objetos Disciplina no arquivo JSON.

    Responsável por salvar e recuperar os dados completos das disciplinas
    (nome, carga horária, obrigatoriedade, pré-requisitos e co-requisitos)
    no arquivo sgsa.json.

    Padrão aplicado: Repository.

    Princípios SOLID:
        - SRP: responsabilidade única de persistir e recuperar disciplinas.

    Exemplo de uso:
        >>> repo = RepositorioDisciplina()
        >>> repo.adicionar(Disciplina("Cálculo I", 72))
        >>> for d in repo.listar():
        ...     print(d)  # ('Cálculo I', 72)
    """

    def adicionar(self, disciplina) -> None:
        """
        Persiste uma nova disciplina no arquivo JSON.

        Salva nome, carga_horaria e obrigatoria. Pré-requisitos e
        co-requisitos são armazenados como listas de nomes.

        :param disciplina: Objeto Disciplina a ser persistido.
        """
        db = load_db()
        # Evita duplicatas pelo nome
        if any(d['nome'].lower() == disciplina.nome.lower() for d in db['disciplinas']):
            print(f"⚠️  Disciplina '{disciplina.nome}' já cadastrada.")
            return

        db['disciplinas'].append({
            "nome": disciplina.nome,
            "carga_horaria": disciplina.carga_horaria,
            "obrigatoria": getattr(disciplina, 'obrigatoria', True),
            "pre_requisitos": [p.nome for p in getattr(disciplina, '_pre_requisitos', [])],
            "co_requisitos": [c.nome for c in getattr(disciplina, '_co_requisitos', [])]
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

    def listar_completo(self) -> list:
        """
        Retorna todas as disciplinas cadastradas como lista de dicionários
        com todos os campos (nome, carga_horaria, obrigatoria,
        pre_requisitos, co_requisitos).

        :return: Lista de dicionários com todos os campos da disciplina.
        """
        db = load_db()
        return db.get('disciplinas', [])

    def buscar_por_nome(self, nome: str) -> dict:
        """
        Busca e retorna o dicionário completo de uma disciplina pelo nome.

        :param nome: Nome da disciplina a buscar (comparação case-insensitive).
        :return: Dicionário com todos os campos, ou None se não encontrado.
        """
        db = load_db()
        for d in db['disciplinas']:
            if d['nome'].lower() == nome.lower():
                return d
        return None

    def atualizar_pre_requisitos(self, nome_disciplina: str,
                                  nomes_pre_requisitos: list) -> None:
        """
        Atualiza a lista de pré-requisitos de uma disciplina no banco.

        :param nome_disciplina: Nome da disciplina a atualizar.
        :param nomes_pre_requisitos: Lista de nomes das disciplinas pré-requisito.
        """
        db = load_db()
        for d in db['disciplinas']:
            if d['nome'].lower() == nome_disciplina.lower():
                d['pre_requisitos'] = nomes_pre_requisitos
                break
        save_db(db)

    def atualizar_co_requisitos(self, nome_disciplina: str,
                                 nomes_co_requisitos: list) -> None:
        """
        Atualiza a lista de co-requisitos de uma disciplina no banco.

        :param nome_disciplina: Nome da disciplina a atualizar.
        :param nomes_co_requisitos: Lista de nomes das disciplinas co-requisito.
        """
        db = load_db()
        for d in db['disciplinas']:
            if d['nome'].lower() == nome_disciplina.lower():
                d['co_requisitos'] = nomes_co_requisitos
                break
        save_db(db)