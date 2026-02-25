from infrastructure.db_config import load_db, save_db


class RepositorioSolicitacao:
    """Persiste e recupera solicitações acadêmicas em arquivo JSON."""

    def adicionar(self, solicitacao, tipo: str):
        db = load_db()

        novo_id = self._gerar_id(db["solicitacoes"])

        nova_solicitacao = {
            "id": novo_id,
            "tipo": tipo,
            "aluno_id": solicitacao.aluno.matricula,
            "status": solicitacao.status,
            "disciplina": solicitacao.disciplina.nome if solicitacao.disciplina else None,
            "curso": solicitacao.curso.nome if solicitacao.curso else None
        }

        db["solicitacoes"].append(nova_solicitacao)
        save_db(db)

    def listar(self):
        db = load_db()

        # Mantendo formato compatível com sua main:
        # (id, tipo, aluno_id, status, disciplina, curso)
        return [
            (
                s["id"],
                s["tipo"],
                s["aluno_id"],
                s["status"],
                s["disciplina"],
                s["curso"]
            )
            for s in db["solicitacoes"]
        ]

    def remover(self, solicitacao_id):
        db = load_db()

        db["solicitacoes"] = [
            s for s in db["solicitacoes"]
            if s["id"] != solicitacao_id
        ]

        save_db(db)

    def atualizar_status(self, solicitacao_id, novo_status):
        db = load_db()

        for s in db["solicitacoes"]:
            if s["id"] == solicitacao_id:
                s["status"] = novo_status
                break

        save_db(db)

    def _gerar_id(self, lista):
        """Simula AUTO_INCREMENT."""
        if not lista:
            return 1
        return max(s["id"] for s in lista) + 1