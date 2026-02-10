from infrastructure.db_config import get_connection

class RepositorioAluno:
    def adicionar(self, aluno):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO alunos (nome, email, matricula, curso) VALUES (?, ?, ?, ?)",
            (aluno.nome, aluno.email, aluno.matricula, aluno.curso._nome)
        )
        conn.commit()
        conn.close()

    def listar(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, email, matricula, curso FROM alunos")
        rows = cursor.fetchall()
        conn.close()
        return rows
