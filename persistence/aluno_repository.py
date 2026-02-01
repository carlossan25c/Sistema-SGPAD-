from persistence.connection import get_connection
from domain.aluno import Aluno

class AlunoRepository:

    def criar_tabela(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS aluno (
                matricula TEXT PRIMARY KEY,
                nome TEXT,
                curso TEXT
            )
        """)
        conn.commit()
        conn.close()

    def salvar(self, aluno: Aluno):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO aluno (matricula, nome, curso)
            VALUES (?, ?, ?)
        """, (aluno.matricula, aluno.nome, aluno.curso))
        conn.commit()
        conn.close()
