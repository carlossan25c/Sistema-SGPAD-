import argparse
import sys
from infrastructure.db_config import init_db, get_connection
from infrastructure.repositorio_aluno import RepositorioAluno
from infrastructure.repositorio_solicitacao import RepositorioSolicitacao
from infrastructure.repositorio_disciplina import RepositorioDisciplina
from application.solicitacao_service import SolicitacaoService
from domain.aluno import Aluno
from domain.curso import Curso
from domain.disciplina import Disciplina

def setup_argparse():
    """
    Configura o parser de argumentos para suportar comandos e subcomandos.
    Estrutura: main.py [comando] [subcomando] [argumentos]
    """
    parser = argparse.ArgumentParser(description="SGSA - Sistema de Gestão de Solicitações Acadêmicas")
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")

    # --- COMANDO: ALUNO ---
    aluno_parser = subparsers.add_parser("aluno", help="Gestão de alunos")
    aluno_sub = aluno_parser.add_subparsers(dest="subcommand")
    
    # Subcomando: aluno cadastrar
    cad_aluno = aluno_sub.add_parser("cadastrar", help="Cadastra um novo aluno")
    cad_aluno.add_argument("--nome", required=True)
    cad_aluno.add_argument("--email", required=True)
    cad_aluno.add_argument("--mat", required=True, help="Matrícula do aluno")
    cad_aluno.add_argument("--curso", required=True)

    # Subcomando: aluno listar
    aluno_sub.add_parser("listar", help="Lista todos os alunos")

    # Subcomando: aluno remover
    rem_aluno = aluno_sub.add_parser("remover", help="Remove um aluno pela matrícula")
    rem_aluno.add_argument("--mat", required=True)

    # --- COMANDO: SOLICITACAO ---
    sol_parser = subparsers.add_parser("solicitacao", help="Gestão de solicitações")
    sol_sub = sol_parser.add_subparsers(dest="subcommand")

    # Subcomando: solicitacao criar
    criar_sol = sol_sub.add_parser("criar", help="Cria uma nova solicitação acadêmica")
    criar_sol.add_argument("--tipo", choices=["matricula", "trancamento", "colacao"], required=True)
    criar_sol.add_argument("--mat", required=True, help="Matrícula do aluno")
    criar_sol.add_argument("--alvo", help="Nome da disciplina ou curso")

    # Subcomando: solicitacao listar
    sol_sub.add_parser("listar", help="Lista todas as solicitações")

    # --- COMANDO: DISCIPLINA ---
    disc_parser = subparsers.add_parser("disciplina", help="Gestão de disciplinas")
    disc_sub = disc_parser.add_subparsers(dest="subcommand")

    # Subcomando: disciplina cadastrar
    cad_disc = disc_sub.add_parser("cadastrar", help="Cadastra uma nova disciplina")
    cad_disc.add_argument("--nome", required=True)
    cad_disc.add_argument("--carga", type=int, required=True)

    return parser

def main():
    """
    Ponto de entrada que processa a lógica de execução baseada nos comandos fornecidos.
    """
    init_db()
    parser = setup_argparse()
    args = parser.parse_args()

    # Repositórios
    repo_aluno = RepositorioAluno()
    repo_solicitacao = RepositorioSolicitacao()
    repo_disciplina = RepositorioDisciplina()
    service = SolicitacaoService()

    if args.command == "aluno":
        if args.subcommand == "cadastrar":
            aluno = Aluno(args.nome, args.email, args.mat, Curso(args.curso))
            repo_aluno.adicionar(aluno)
            print(f"✅ Aluno {args.nome} cadastrado!")
        
        elif args.subcommand == "listar":
            for a in repo_aluno.listar():
                print(f"ID: {a[2]} | Nome: {a[0]} | Curso: {a[3]}")

        elif args.subcommand == "remover":
            conn = get_connection()
            conn.execute("DELETE FROM alunos WHERE matricula = ?", (args.mat,))
            conn.commit()
            print(f"🗑️ Aluno {args.mat} removido.")

    elif args.command == "solicitacao":
        if args.subcommand == "criar":
            # Nota: Em um sistema real, buscaríamos o objeto Aluno real no DB aqui
            aluno_mock = Aluno("Estudante", "email@u.com", args.mat, Curso("Geral"))
            sol = service.criar_solicitacao(args.tipo, aluno_mock, args.alvo)
            repo_solicitacao.adicionar(sol, args.tipo)
            print(f"✅ Solicitação de {args.tipo} criada para {args.mat}!")

        elif args.subcommand == "listar":
            for s in repo_solicitacao.listar():
                print(f"ID: {s[0]} | Tipo: {s[1]} | Status: {s[3]}")

    elif args.command == "disciplina":
        if args.subcommand == "cadastrar":
            repo_disciplina.adicionar(Disciplina(args.nome, args.carga))
            print(f"✅ Disciplina {args.nome} cadastrada!")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()