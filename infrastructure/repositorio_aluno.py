# infrastructure/repositorio_aluno.py
"""
Módulo que implementa o repositório de persistência de alunos.
"""

from infrastructure.db_config import load_db, save_db


class RepositorioAluno:
    """
    Gerencia a persistência de objetos Aluno no arquivo JSON.
    Persiste dados cadastrais incluindo limite de horas semestrais
    e mínimo de horas optativas do curso.
    """

    def adicionar(self, aluno) -> None:
        """Persiste um novo aluno. Bloqueia matrícula duplicada."""
        db = load_db()
        if any(a['matricula'] == aluno.matricula for a in db['alunos']):
            print(f"⚠️  Matrícula {aluno.matricula} já existe.")
            return
        db['alunos'].append({
            "nome": aluno.nome,
            "email": aluno.email,
            "matricula": aluno.matricula,
            "curso": aluno.curso.nome,
            "limite_horas_semestrais": getattr(aluno.curso, 'limite_horas_semestrais', 360),
            "min_horas_optativas": getattr(aluno.curso, 'min_horas_optativas', 0)
        })
        save_db(db)

    def listar(self) -> list:
        """Retorna lista de tuplas (nome, email, matricula, curso)."""
        db = load_db()
        return [
            (a['nome'], a['email'], a['matricula'], a['curso'],
             a.get('limite_horas_semestrais', 360),
             a.get('min_horas_optativas', 0))
            for a in db['alunos']
        ]

    def remover(self, matricula: str) -> None:
        """Remove um aluno pela matrícula."""
        db = load_db()
        original = len(db['alunos'])
        db['alunos'] = [a for a in db['alunos'] if a['matricula'] != matricula]
        if len(db['alunos']) < original:
            save_db(db)
            print(f"✅ Aluno {matricula} removido.")
        else:
            print(f"⚠️ Aluno com matrícula '{matricula}' não encontrado.")