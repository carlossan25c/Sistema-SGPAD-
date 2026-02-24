# infrastructure/repositorio_disciplina.py
from infrastructure.db_config import get_connection

class RepositorioDisciplina:
    """
    Responsável pela persistência e recuperação de dados de disciplinas no banco de dados.
    """
    def adicionar(self, disciplina):
        """Insere uma nova disciplina (nome e carga horária) no sistema."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO disciplinas (nome, carga_horaria)
            VALUES (?, ?)
        """, (disciplina.nome, disciplina.carga_horaria))
        conn.commit()
        conn.close()

    def listar(self):
        """Recupera a lista completa de disciplinas cadastradas."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nome, carga_horaria FROM disciplinas")
        disciplinas = cursor.fetchall()
        conn.close()
        return disciplinas
