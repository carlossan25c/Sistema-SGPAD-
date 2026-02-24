# infrastructure/repositorio_solicitacao.py
from infrastructure.db_config import get_connection

class RepositorioSolicitacao:
    """Persiste e recupera solicitações acadêmicas do banco."""
    def adicionar(self, solicitacao, tipo: str):
        """
        Salva uma solicitação. Nota: Atributos disciplina/curso 
        podem ser nulos dependendo do tipo da solicitação.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO solicitacoes (tipo, aluno_id, status, disciplina, curso)
            VALUES (?, ?, ?, ?, ?)
        """, (
            tipo,  # usa o parâmetro recebido
            solicitacao.aluno.matricula,  # referência ao aluno
            solicitacao.status,
            solicitacao.disciplina.nome if solicitacao.disciplina else None,
            solicitacao.curso.nome if solicitacao.curso else None
        ))
        conn.commit()
        conn.close()

    def listar(self):
        """Retorna o histórico bruto de todas as solicitações."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, tipo, aluno_id, status, disciplina, curso FROM solicitacoes")
        solicitacoes = cursor.fetchall()
        conn.close()
        return solicitacoes
