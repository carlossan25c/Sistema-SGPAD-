# infrastructure/repositorio_disciplina.py
"""
Módulo que implementa o repositório de persistência de disciplinas.

Gerencia as operações de leitura e escrita de disciplinas no arquivo JSON,
incluindo pré-requisitos, co-requisitos, obrigatoriedade e carga horária.
"""

from infrastructure.db_config import load_db, save_db


class RepositorioDisciplina:
    """
    Gerencia a persistência de objetos Disciplina no arquivo JSON.

    Persiste todos os atributos relevantes: nome, carga_horaria, obrigatoria,
    pre_requisitos e co_requisitos (como listas de nomes). Ao carregar,
    reconstrói os vínculos entre objetos Disciplina automaticamente.
    """

    def adicionar(self, disciplina) -> None:
        """
        Persiste uma disciplina no JSON com todos os seus atributos.

        :param disciplina: Objeto Disciplina a ser persistido.
        """
        db = load_db()
        # Evita duplicata por nome
        if any(d['nome'] == disciplina.nome for d in db['disciplinas']):
            print(f"⚠️  Disciplina '{disciplina.nome}' já existe.")
            return
        db['disciplinas'].append({
            "nome": disciplina.nome,
            "carga_horaria": disciplina.carga_horaria,
            "obrigatoria": disciplina.obrigatoria,
            "pre_requisitos": [p.nome for p in disciplina.pre_requisitos],
            "co_requisitos": [c.nome for c in disciplina.co_requisitos],
        })
        save_db(db)

    def listar(self) -> list:
        """
        Retorna todas as disciplinas como lista de tuplas (nome, carga_horaria).
        """
        db = load_db()
        return [(d['nome'], d['carga_horaria']) for d in db['disciplinas']]

    def carregar_todas(self) -> dict:
        """
        Carrega todas as disciplinas do JSON e reconstrói os vínculos de
        pré-requisitos e co-requisitos entre os objetos.

        :return: Dicionário {nome: Disciplina} com todos os objetos reconstruídos.
        """
        from domain.disciplina import Disciplina
        db = load_db()
        # Primeira passagem: cria todos os objetos sem vínculos
        disciplinas = {
            d['nome']: Disciplina(d['nome'], d['carga_horaria'], d.get('obrigatoria', True))
            for d in db['disciplinas']
        }
        # Segunda passagem: reconstrói os vínculos
        for d in db['disciplinas']:
            obj = disciplinas[d['nome']]
            for pre in d.get('pre_requisitos', []):
                if pre in disciplinas:
                    obj.adicionar_pre_requisito(disciplinas[pre])
            for co in d.get('co_requisitos', []):
                if co in disciplinas:
                    obj.adicionar_co_requisito(disciplinas[co])
        return disciplinas
