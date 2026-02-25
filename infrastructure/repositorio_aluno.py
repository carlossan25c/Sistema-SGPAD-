from infrastructure.db_config import load_db, save_db

class RepositorioAluno:
    """Gere a persistência de Alunos no ficheiro JSON."""

    def adicionar(self, aluno):
        db = load_db()
        # Verifica se a matrícula já existe
        if any(a['matricula'] == aluno.matricula for a in db['alunos']):
            print(f"⚠️ Erro: Matrícula {aluno.matricula} já existe.")
            return
        
        db['alunos'].append({
            "nome": aluno.nome,
            "email": aluno.email,
            "matricula": aluno.matricula,
            "curso": aluno.curso.nome
        })
        save_db(db)

    def listar(self):
        db = load_db()
        # Retorna uma lista de tuplos para manter compatibilidade com a main antiga se necessário
        return [(a['nome'], a['email'], a['matricula'], a['curso']) for a in db['alunos']]

    def remover(self, matricula):
        db = load_db()
        original_count = len(db['alunos'])
        db['alunos'] = [a for a in db['alunos'] if a['matricula'] != matricula]
        if len(db['alunos']) < original_count:
            save_db(db)
            print(f"✅ Aluno {matricula} removido.")
        else:
            print(f"⚠️ Aluno {matricula} não encontrado.")