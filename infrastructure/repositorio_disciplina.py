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
        if any(d['nome'].lower() == disciplina.nome.lower() for d in db['disciplinas']):
            print(f"Disciplina '{disciplina.nome}' ja cadastrada.")
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
        """Retorna todas as disciplinas como lista de tuplas (nome, carga_horaria)."""
        db = load_db()
        return [(d['nome'], d['carga_horaria']) for d in db['disciplinas']]

    def listar_completo(self) -> list:
        """Retorna todas as disciplinas como lista de dicionários completos."""
        db = load_db()
        return db.get('disciplinas', [])

    def carregar_todas(self) -> dict:
        """
        Carrega todas as disciplinas do JSON e reconstrói os vínculos de
        pré-requisitos e co-requisitos entre os objetos.

        :return: Dicionário {nome: Disciplina} com todos os objetos reconstruídos.
        """
        from domain.disciplina import Disciplina
        db = load_db()
        disciplinas = {
            d['nome']: Disciplina(d['nome'], d['carga_horaria'], d.get('obrigatoria', True))
            for d in db['disciplinas']
        }
        for d in db['disciplinas']:
            obj = disciplinas[d['nome']]
            for pre in d.get('pre_requisitos', []):
                if pre in disciplinas:
                    obj.adicionar_pre_requisito(disciplinas[pre])
            for co in d.get('co_requisitos', []):
                if co in disciplinas:
                    obj.adicionar_co_requisito(disciplinas[co])
        return disciplinas

    def buscar_por_nome(self, nome: str) -> dict:
        """Busca e retorna o dicionário completo de uma disciplina pelo nome."""
        db = load_db()
        for d in db['disciplinas']:
            if d['nome'].lower() == nome.lower():
                return d
        return None

    def atualizar_pre_requisitos(self, nome_disciplina: str, nomes_pre_requisitos: list) -> None:
        """Atualiza a lista de pré-requisitos de uma disciplina no banco."""
        db = load_db()
        for d in db['disciplinas']:
            if d['nome'].lower() == nome_disciplina.lower():
                d['pre_requisitos'] = nomes_pre_requisitos
                break
        save_db(db)

    def atualizar_co_requisitos(self, nome_disciplina: str, nomes_co_requisitos: list) -> None:
        """Atualiza a lista de co-requisitos de uma disciplina no banco."""
        db = load_db()
        for d in db['disciplinas']:
            if d['nome'].lower() == nome_disciplina.lower():
                d['co_requisitos'] = nomes_co_requisitos
                break
        save_db(db)
