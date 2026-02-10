from infrastructure.db_config import get_connection

class RepositorioSolicitacao:
    def adicionar(self, solicitacao, tipo):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO solicitacoes (tipo, aluno_id, status, disciplina, curso) VALUES (?, ?, ?, ?, ?)",
            (
                tipo,
                solicitacao.aluno.id if hasattr(solicitacao.aluno, "id") else 1,  # simplificação
                solicitacao.status,
                getattr(solicitacao, "_disciplina", None)._codigo if hasattr(solicitacao, "_disciplina") else None,
                getattr(solicitacao, "_curso", None)._nome if hasattr(solicitacao, "_curso") else None
            )
        )
        conn.commit()
        conn.close()

    def listar(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, tipo, aluno_id, status, disciplina, curso FROM solicitacoes")
        rows = cursor.fetchall()
        conn.close()
        return rows
