from persistence.connection import get_connection

class SolicitacaoRepository:

    def criar_tabela(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS solicitacao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT,
                estado TEXT,
                aluno_matricula TEXT
            )
        """)
        conn.commit()
        conn.close()

    def salvar(self, solicitacao):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO solicitacao (tipo, estado, aluno_matricula)
            VALUES (?, ?, ?)
        """, (
            solicitacao.__class__.__name__,
            solicitacao._estado.__class__.__name__,
            solicitacao._aluno.matricula
        ))
        conn.commit()
        conn.close()
