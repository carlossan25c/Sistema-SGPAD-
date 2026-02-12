# infrastructure/repositorio_aluno.py
from infrastructure.db_config import get_connection

class RepositorioAluno:
    def adicionar(self, aluno):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alunos (nome, email, matricula, curso)
            VALUES (?, ?, ?, ?)
        """, (aluno.nome, aluno.email, aluno.matricula, aluno.curso.nome))
        conn.commit()
        conn.close()

    def listar(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nome, email, matricula, curso FROM alunos")
        alunos = cursor.fetchall()
        conn.close()
        return alunos
