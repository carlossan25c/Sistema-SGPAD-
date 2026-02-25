from infrastructure.db_config import load_db, save_db


class RepositorioDisciplina:
    """
    Responsável pela persistência e recuperação de dados
    de disciplinas no arquivo JSON.
    """

    def adicionar(self, disciplina):
        db = load_db()

        nova_disciplina = {
            "id": self._gerar_id(db["disciplinas"]),
            "nome": disciplina.nome,
            "carga_horaria": disciplina.carga_horaria
        }

        db["disciplinas"].append(nova_disciplina)
        save_db(db)

    def listar(self):
        db = load_db()

        # Mantendo formato compatível com sua main:
        # (nome, carga_horaria)
        return [
            (d["nome"], d["carga_horaria"])
            for d in db["disciplinas"]
        ]

    def remover(self, nome_disciplina):
        db = load_db()

        db["disciplinas"] = [
            d for d in db["disciplinas"]
            if d["nome"] != nome_disciplina
        ]

        save_db(db)

    def _gerar_id(self, lista):
        """Simula AUTO_INCREMENT."""
        if not lista:
            return 1
        return max(d["id"] for d in lista) + 1