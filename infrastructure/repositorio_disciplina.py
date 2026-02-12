# infrastructure/repositorio_disciplina.py
from infrastructure.db_config import get_connection

class RepositorioDisciplina:
    def adicionar(self, disciplina):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO disciplinas (nome, carga_horaria)
            VALUES (?, ?)
        """, (disciplina.nome, disciplina.carga_horaria))
        conn.commit()
        conn.close()

    def listar(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nome, carga_horaria FROM disciplinas")
        disciplinas = cursor.fetchall()
        conn.close()
        return disciplinas
