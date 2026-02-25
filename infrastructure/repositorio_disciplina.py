from infrastructure.db_config import load_db, save_db

class RepositorioDisciplina:
    """Gere a persistência de Disciplinas no ficheiro JSON."""

    def adicionar(self, disciplina):
        db = load_db()
        db['disciplinas'].append({
            "nome": disciplina.nome,
            "carga_horaria": disciplina.carga_horaria
        })
        save_db(db)

    def listar(self):
        db = load_db()
        return [(d['nome'], d['carga_horaria']) for d in db['disciplinas']]