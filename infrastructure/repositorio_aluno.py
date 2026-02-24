# infrastructure/repositorio_aluno.py
from infrastructure.db_config import get_connection

class RepositorioAluno:
    """Gerencia a persistência de objetos Aluno no banco de dados."""
    def adicionar(self, aluno):
        """Insere um novo aluno no banco."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alunos (nome, email, matricula, curso)
            VALUES (?, ?, ?, ?)
        """, (aluno.nome, aluno.email, aluno.matricula, aluno.curso.nome))
        conn.commit()
        conn.close()

    def listar(self):
        """Retorna todos os alunos cadastrados."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nome, email, matricula, curso FROM alunos")
        alunos = cursor.fetchall()
        conn.close()
        return alunos
