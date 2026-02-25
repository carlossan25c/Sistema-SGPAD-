from infrastructure.db_config import load_db, save_db

class RepositorioSolicitacao:
    """Gere a persistência de Solicitações no ficheiro JSON."""

    def adicionar(self, solicitacao, tipo: str):
        db = load_db()
        nova_sol = {
            "id": len(db['solicitacoes']) + 1,
            "tipo": tipo,
            "aluno_id": solicitacao.aluno.matricula,
            "status": solicitacao.status,
            "alvo": solicitacao.disciplina.nome if hasattr(solicitacao, '_disciplina') and solicitacao._disciplina else 
                    (solicitacao._curso.nome if hasattr(solicitacao, '_curso') and solicitacao._curso else "N/A")
        }
        db['solicitacoes'].append(nova_sol)
        save_db(db)

    def listar(self):
        db = load_db()
        return [(s['id'], s['tipo'], s['aluno_id'], s['status'], s['alvo']) for s in db['solicitacoes']]