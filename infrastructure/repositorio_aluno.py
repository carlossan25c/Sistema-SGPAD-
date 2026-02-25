from infrastructure.db_config import load_db, save_db


class RepositorioAluno:
    """Gerencia a persistência de objetos Aluno em arquivo JSON."""

    def adicionar(self, aluno):
        db = load_db()

        # Verifica se matrícula já existe (simulando PRIMARY KEY)
        for a in db["alunos"]:
            if a["matricula"] == aluno.matricula:
                print("⚠️ Matrícula já cadastrada.")
                return

        novo_aluno = {
            "nome": aluno.nome,
            "email": aluno.email,
            "matricula": aluno.matricula,
            "curso": aluno.curso.nome
        }

        db["alunos"].append(novo_aluno)
        save_db(db)

    def listar(self):
        db = load_db()

        # Mantendo o mesmo formato que você usava (tupla estilo SQL)
        return [
            (a["nome"], a["email"], a["matricula"], a["curso"])
            for a in db["alunos"]
        ]

    def remover(self, matricula):
        db = load_db()

        alunos_filtrados = [
            a for a in db["alunos"]
            if a["matricula"] != matricula
        ]

        db["alunos"] = alunos_filtrados
        save_db(db)