import argparse
from infrastructure.db_config import init_db
from infrastructure.repositorio_aluno import RepositorioAluno
from infrastructure.repositorio_solicitacao import RepositorioSolicitacao
from infrastructure.repositorio_disciplina import RepositorioDisciplina
from application.solicitacao_service import SolicitacaoService
from domain.aluno import Aluno
from domain.curso import Curso
from domain.disciplina import Disciplina

def setup_argparse():
    """Configura a interface de linha de comando com argparse."""
    parser = argparse.ArgumentParser(description="SGSA - Sistema de Gestão Académica (Versão JSON)")
    subparsers = parser.add_subparsers(dest="command", help="Comandos principais")

    # Comando Aluno
    aluno_p = subparsers.add_parser("aluno", help="Gestão de alunos")
    aluno_sub = aluno_p.add_subparsers(dest="subcommand")
    
    cad = aluno_sub.add_parser("cadastrar", help="Cadastrar aluno")
    cad.add_argument("--nome", required=True)
    cad.add_argument("--email", required=True)
    cad.add_argument("--mat", required=True)
    cad.add_argument("--curso", required=True)

    aluno_sub.add_parser("listar", help="Listar alunos")
    
    rem = aluno_sub.add_parser("remover", help="Remover aluno")
    rem.add_argument("--mat", required=True)

    # Comando Disciplina
    disc_p = subparsers.add_parser("disciplina", help="Gestão de disciplinas")
    disc_sub = disc_p.add_subparsers(dest="subcommand")
    
    cad_d = disc_sub.add_parser("cadastrar", help="Cadastrar disciplina")
    cad_d.add_argument("--nome", required=True)
    cad_d.add_argument("--carga", type=int, required=True)
    
    disc_sub.add_parser("listar", help="Listar disciplinas")

    # Comando Solicitação
    sol_p = subparsers.add_parser("solicitacao", help="Gestão de solicitações")
    sol_sub = sol_p.add_subparsers(dest="subcommand")
    
    criar = sol_sub.add_parser("criar", help="Criar solicitação")
    criar.add_argument("--tipo", choices=["matricula", "trancamento", "colacao"], required=True)
    criar.add_argument("--mat", required=True)
    criar.add_argument("--alvo", required=True)

    sol_sub.add_parser("listar", help="Listar solicitações")

    return parser

def main():
    """Executa o sistema com base nos argumentos passados."""
    init_db()
    parser = setup_argparse()
    args = parser.parse_args()

    repo_aluno = RepositorioAluno()
    repo_disc = RepositorioDisciplina()
    repo_sol = RepositorioSolicitacao()
    service = SolicitacaoService()

    if args.command == "aluno":
        if args.subcommand == "cadastrar":
            aluno = Aluno(args.nome, args.email, args.mat, Curso(args.curso))
            repo_aluno.adicionar(aluno)
            print(f"✅ Aluno {args.nome} guardado no ficheiro JSON!")
        elif args.subcommand == "listar":
            print("\n📋 Lista de Alunos (JSON):")
            for a in repo_aluno.listar():
                print(f" - {a[0]} | Mat: {a[2]} | Curso: {a[3]}")
        elif args.subcommand == "remover":
            repo_aluno.remover(args.mat)

    elif args.command == "disciplina":
        if args.subcommand == "cadastrar":
            repo_disc.adicionar(Disciplina(args.nome, args.carga))
            print(f"✅ Disciplina {args.nome} adicionada.")
        elif args.subcommand == "listar":
            for d in repo_disc.listar():
                print(f" - {d[0]} ({d[1]}h)")

    elif args.command == "solicitacao":
        if args.subcommand == "criar":
            aluno_obj = Aluno("Estudante", "email", args.mat, Curso("Geral"))
            sol = service.criar_solicitacao(args.tipo, aluno_obj, args.alvo)
            repo_sol.adicionar(sol, args.tipo)
            print(f"✅ Solicitação de {args.tipo} registada.")
        elif args.subcommand == "listar":
            for s in repo_sol.listar():
                print(f"ID: {s[0]} | Tipo: {s[1]} | Aluno: {s[2]} | Alvo: {s[4]} | Status: {s[3]}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()