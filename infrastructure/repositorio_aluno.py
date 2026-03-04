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
<<<<<<< HEAD
            "limite_horas_semestrais": aluno.curso.limite_horas_semestrais,
            "min_horas_optativas": aluno.curso.min_horas_optativas,
=======
            "limite_horas_semestrais": getattr(aluno.curso, 'limite_horas_semestrais', 360),
            "min_horas_optativas": getattr(aluno.curso, 'min_horas_optativas', 0)
>>>>>>> 147dd71905465b27027101eac65fdb6e2035acd2
        })
        save_db(db)

    def listar(self) -> list:
        """Retorna lista de tuplas (nome, email, matricula, curso)."""
        db = load_db()
<<<<<<< HEAD
        return [(a['nome'], a['email'], a['matricula'], a['curso'])
                for a in db['alunos']]

    def buscar(self, matricula: str):
        """
        Busca e reconstrói um objeto Aluno completo a partir do JSON.

        :param matricula: Matrícula a buscar.
        :return: Objeto Aluno com Curso configurado, ou None se não encontrado.
        """
        from domain.aluno import Aluno
        from domain.curso import Curso
        db = load_db()
        registro = next((a for a in db['alunos'] if a['matricula'] == matricula), None)
        if not registro:
            return None
        curso = Curso(
            registro['curso'],
            limite_horas_semestrais=registro.get('limite_horas_semestrais', 360),
            min_horas_optativas=registro.get('min_horas_optativas', 0),
        )
        return Aluno(registro['nome'], registro['email'], registro['matricula'], curso)
=======
        return [
            (a['nome'], a['email'], a['matricula'], a['curso'],
             a.get('limite_horas_semestrais', 360),
             a.get('min_horas_optativas', 0))
            for a in db['alunos']
        ]
>>>>>>> 147dd71905465b27027101eac65fdb6e2035acd2

    def remover(self, matricula: str) -> None:
        """Remove um aluno pela matrícula."""
        db = load_db()
        original = len(db['alunos'])
        db['alunos'] = [a for a in db['alunos'] if a['matricula'] != matricula]
        if len(db['alunos']) < original:
            save_db(db)
            print(f"✅ Aluno {matricula} removido.")
        else:
<<<<<<< HEAD
            print(f"⚠️  Aluno '{matricula}' não encontrado.")
=======
            print(f"⚠️ Aluno com matrícula '{matricula}' não encontrado.")
>>>>>>> 147dd71905465b27027101eac65fdb6e2035acd2
