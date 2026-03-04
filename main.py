# main.py
"""
Ponto de entrada da aplicação SGSA — Interface de Linha de Comando (CLI).

Uso básico:
    python main.py aluno cadastrar --nome "João" --email "j@email.com" --mat "001" --curso "ADS"
    python main.py aluno cadastrar --nome "João" ... --limite-horas 200 --min-optativas 120
    python main.py disciplina cadastrar --nome "Cálculo II" --carga 72 --pre-req "Cálculo I"
    python main.py disciplina cadastrar --nome "Física Teórica" --carga 60 --co-req "Lab. Física"
    python main.py solicitacao criar --tipo matricula --mat "001" --alvo "Cálculo II"
    python main.py solicitacao criar --tipo matricula --mat "001" --alvo "Cálculo II" --carga-atual 100
    python main.py solicitacao criar --tipo trancamento --mat "001" --alvo "Cálculo I" --prazo 2025-10-31
    python main.py solicitacao criar --tipo colacao --mat "001" --alvo "ADS"
    python main.py demo
"""

import argparse
import datetime

from infrastructure.db_config import init_db
from infrastructure.repositorio_aluno import RepositorioAluno
from infrastructure.repositorio_solicitacao import RepositorioSolicitacao
from infrastructure.repositorio_disciplina import RepositorioDisciplina

from application.solicitacao_service import SolicitacaoService
from application.notificacao_service import NotificacaoService

from domain.aluno import Aluno
from domain.curso import Curso
from domain.disciplina import Disciplina
from domain.excecoes import ViolacaoRegraAcademicaError

from rules.regra_pre_requisito import RegraPreRequisito
from rules.regra_co_requisito import RegraCoRequisito
from rules.regra_limite_carga_horaria import RegraLimiteCargaHoraria
from rules.regra_prazo import RegraPrazo
from rules.regra_limite_trancamentos import RegraLimiteTrancamentos
from rules.regra_vinculo_ativo import RegraVinculoAtivo
from rules.regra_elegibilidade import RegraElegibilidade
from rules.regra_pendencia_documentacao import RegraPendenciaDocumentacao

REGRAS_POR_TIPO = {
    "matricula": [
        RegraPreRequisito(),
        RegraCoRequisito(),
        RegraLimiteCargaHoraria(),
    ],
    "trancamento": [
        RegraPrazo(),
        RegraLimiteTrancamentos(),
        RegraVinculoAtivo(),
    ],
    "colacao": [
        RegraElegibilidade(),
        RegraPendenciaDocumentacao(),
    ],
}


def setup_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SGSA - Sistema de Gestão Académica")
    subparsers = parser.add_subparsers(dest="command", help="Comandos principais")

    # ---- aluno ----
    aluno_p = subparsers.add_parser("aluno", help="Gestão de alunos")
    aluno_sub = aluno_p.add_subparsers(dest="subcommand")

    cad = aluno_sub.add_parser("cadastrar", help="Cadastrar novo aluno")
    cad.add_argument("--nome", required=True)
    cad.add_argument("--email", required=True)
    cad.add_argument("--mat", required=True)
    cad.add_argument("--curso", required=True)
    cad.add_argument("--limite-horas", type=int, default=360,
                     help="Limite de carga horária semestral do curso (padrão: 360h)")
    cad.add_argument("--min-optativas", type=int, default=0,
                     help="Mínimo de horas optativas para colação (padrão: 0)")

    aluno_sub.add_parser("listar")

    rem = aluno_sub.add_parser("remover")
    rem.add_argument("--mat", required=True)

    # ---- disciplina ----
    disc_p = subparsers.add_parser("disciplina", help="Gestão de disciplinas")
    disc_sub = disc_p.add_subparsers(dest="subcommand")

    cad_d = disc_sub.add_parser("cadastrar", help="Cadastrar nova disciplina")
    cad_d.add_argument("--nome", required=True)
    cad_d.add_argument("--carga", type=int, required=True)
    cad_d.add_argument("--pre-req", default=None,
                       help="Nome da disciplina pré-requisito (deve já estar cadastrada)")
    cad_d.add_argument("--co-req", default=None,
                       help="Nome da disciplina co-requisito (deve já estar cadastrada)")
    cad_d.add_argument("--optativa", action="store_true",
                       help="Marcar disciplina como optativa (padrão: obrigatória)")

    disc_sub.add_parser("listar")

    # ---- solicitacao ----
    sol_p = subparsers.add_parser("solicitacao", help="Gestão de solicitações")
    sol_sub = sol_p.add_subparsers(dest="subcommand")

    criar = sol_sub.add_parser("criar", help="Criar e validar nova solicitação")
    criar.add_argument("--tipo", choices=["matricula", "trancamento", "colacao"], required=True)
    criar.add_argument("--mat", required=True, help="Matrícula do aluno solicitante")
    criar.add_argument("--alvo", required=True, help="Nome da disciplina ou curso")
    criar.add_argument("--prazo", default=None,
                       help="Prazo acadêmico formato YYYY-MM-DD (trancamento)")
    criar.add_argument("--carga-atual", type=int, default=0,
                       help="Horas já matriculadas no semestre (matrícula)")

    sol_sub.add_parser("listar")

    # ---- demo ----
    subparsers.add_parser("demo", help="Executa todos os cenários de demonstração automaticamente")

    return parser


def _criar_solicitacao(args, repo_aluno, repo_disc, repo_sol, service):
    """
    Núcleo do comando 'solicitacao criar'.

    Busca o aluno e a disciplina reais do JSON (com todos os vínculos
    de pré/co-requisitos e configurações do curso), monta a solicitação
    e aplica as regras acadêmicas correspondentes.
    """
    # 1. Busca aluno real no JSON (com curso configurado)
    aluno = repo_aluno.buscar(args.mat)
    if not aluno:
        print(f"❌ Aluno com matrícula '{args.mat}' não encontrado. Cadastre-o primeiro.")
        return

    # 2. Carrega todas as disciplinas do JSON com pré/co-requisitos reconstituídos
    todas_disciplinas = repo_disc.carregar_todas()

    # 3. Resolve o alvo (disciplina ou curso)
    if args.tipo in ("matricula", "trancamento"):
        alvo = todas_disciplinas.get(args.alvo)
        if not alvo:
            print(f"❌ Disciplina '{args.alvo}' não encontrada. Cadastre-a primeiro.")
            return
    else:
        # Colação: alvo é o Curso do próprio aluno
        alvo = aluno.curso

    # 4. Kwargs extras por tipo
    kwargs = {}
    if args.tipo == "trancamento" and args.prazo:
        kwargs["prazo"] = datetime.date.fromisoformat(args.prazo)
    if args.tipo == "matricula":
        kwargs_sol = {}  # não passa no construtor, define depois
    
    # 5. Cria e valida
    try:
        sol = service.criar_solicitacao(args.tipo, aluno, alvo, **kwargs)

        # Informa carga atual do semestre para RegraLimiteCargaHoraria
        if args.tipo == "matricula":
            sol.carga_horaria_semestre_atual = args.carga_atual

        regras = REGRAS_POR_TIPO.get(args.tipo, [])
        service.aplicar_regras(sol, regras)
        repo_sol.adicionar(sol, args.tipo)
        print(f"✅ Solicitação de '{args.tipo}' registrada e validada com sucesso.")
    except ViolacaoRegraAcademicaError as e:
        print(f"❌ {e}")


def _demo(repo_aluno, repo_disc, repo_sol, service):
    """
    Executa automaticamente todos os cenários de aceite e negação.
    Exige que os alunos e disciplinas já estejam cadastrados via CLI.
    """
    from domain.historico import Historico

    todas = repo_disc.carregar_todas()

    cenarios = [
        # (descrição, tipo, mat, nome_alvo, kwargs_extra, carga_atual, deve_passar)
        ("Matrícula simples sem restrições",             "matricula",   "MAT001", "Programação Orientada a Objetos", {}, 0,   True),
        ("Matrícula com pré-requisito não cumprido",     "matricula",   "MAT002", "Cálculo II",          {}, 0,   False),
        ("Matrícula com co-requisito não atendido",      "matricula",   "MAT003", "Física Teórica",      {}, 0,   False),
        ("Matrícula excedendo carga horária semestral",  "matricula",   "MAT004", "Projeto de Sistemas", {}, 100, False),
        ("Trancamento dentro do prazo",                  "trancamento", "TRA001", "Banco de Dados",      {"prazo": datetime.date(2026, 12, 31)}, 0, True),
        ("Trancamento fora do prazo",                    "trancamento", "TRA001", "Banco de Dados",      {"prazo": datetime.date(2026, 1, 1)},  0, False),
        ("Colação sem créditos suficientes",             "colacao",     "COL001", None,                  {}, 0,  False),
    ]

    # Cenário especial: colação aprovada — criamos aluno com histórico completo em memória
    tcc = todas.get("TCC")
    poo = todas.get("POO")
    aluno_apto = repo_aluno.buscar("COL001")

    print("\n" + "=" * 65)
    print("  DEMO — CENÁRIOS AUTOMÁTICOS")
    print("=" * 65)

    for descricao, tipo, mat, nome_alvo, kwargs, carga_atual, deve_passar in cenarios:
        aluno = repo_aluno.buscar(mat)
        if not aluno:
            print(f"  ⚠️  Aluno '{mat}' não encontrado — pule para o próximo.")
            continue

        if tipo in ("matricula", "trancamento"):
            alvo = todas.get(nome_alvo)
            if not alvo:
                print(f"  ⚠️  Disciplina '{nome_alvo}' não encontrada.")
                continue
        else:
            alvo = aluno.curso

        try:
            sol = service.criar_solicitacao(tipo, aluno, alvo, **kwargs)
            if tipo == "matricula":
                sol.carga_horaria_semestre_atual = carga_atual
            service.aplicar_regras(sol, REGRAS_POR_TIPO[tipo])
            repo_sol.adicionar(sol, tipo)
            resultado = "✅ APROVADO" if deve_passar else "❌ DEVERIA TER SIDO NEGADO"
        except ViolacaoRegraAcademicaError as e:
            resultado = "✅ NEGADO corretamente" if not deve_passar else f"❌ DEVERIA TER PASSADO — {e}"

        print(f"\n  [{resultado}]")
        print(f"  Cenário : {descricao}")

    # Cenário extra: colação aprovada com histórico completo
    if aluno_apto and tcc and poo:
        aluno_apto.historico.adicionar_disciplina(tcc, 8.0)
        if poo:
            aluno_apto.historico.adicionar_disciplina(poo, 7.0)
        try:
            sol = service.criar_solicitacao("colacao", aluno_apto, aluno_apto.curso)
            service.aplicar_regras(sol, REGRAS_POR_TIPO["colacao"])
            repo_sol.adicionar(sol, "colacao")
            print(f"\n  [✅ APROVADO]")
            print(f"  Cenário : Colação com histórico completo e sem pendências")
        except ViolacaoRegraAcademicaError as e:
            print(f"\n  [❌ DEVERIA TER PASSADO — {e}]")
            print(f"  Cenário : Colação com histórico completo e sem pendências")

    print("\n" + "=" * 65 + "\n")


def main() -> None:
    init_db()
    parser = setup_argparse()
    args = parser.parse_args()

    repo_aluno = RepositorioAluno()
    repo_disc = RepositorioDisciplina()
    repo_sol = RepositorioSolicitacao()
    notificacao = NotificacaoService()
    service = SolicitacaoService(notificacao_service=notificacao)

    if args.command == "aluno":
        if args.subcommand == "cadastrar":
            curso = Curso(
                args.curso,
                limite_horas_semestrais=args.limite_horas,
                min_horas_optativas=args.min_optativas,
            )
            aluno = Aluno(args.nome, args.email, args.mat, curso)
            repo_aluno.adicionar(aluno)
            print(f"✅ Aluno '{args.nome}' guardado com sucesso!")
        elif args.subcommand == "listar":
            print("\n📋 Lista de Alunos:")
            for a in repo_aluno.listar():
                print(f"  - {a[0]} | Mat: {a[2]} | Curso: {a[3]}")
        elif args.subcommand == "remover":
            repo_aluno.remover(args.mat)

    elif args.command == "disciplina":
        if args.subcommand == "cadastrar":
            todas = repo_disc.carregar_todas()
            nova = Disciplina(args.nome, args.carga, obrigatoria=not args.optativa)

            if args.pre_req:
                pre = todas.get(args.pre_req)
                if not pre:
                    print(f"❌ Pré-requisito '{args.pre_req}' não encontrado. Cadastre-o primeiro.")
                    return
                nova.adicionar_pre_requisito(pre)

            if args.co_req:
                co = todas.get(args.co_req)
                if not co:
                    print(f"❌ Co-requisito '{args.co_req}' não encontrado. Cadastre-o primeiro.")
                    return
                nova.adicionar_co_requisito(co)

            repo_disc.adicionar(nova)
            print(f"✅ Disciplina '{args.nome}' adicionada.")
        elif args.subcommand == "listar":
            print("\n📚 Lista de Disciplinas:")
            for d in repo_disc.listar():
                print(f"  - {d[0]} ({d[1]}h)")

    elif args.command == "solicitacao":
        if args.subcommand == "criar":
            _criar_solicitacao(args, repo_aluno, repo_disc, repo_sol, service)
        elif args.subcommand == "listar":
            print("\n📄 Lista de Solicitações:")
            for s in repo_sol.listar():
                print(
                    f"  ID: {s[0]} | Tipo: {s[1]} | "
                    f"Aluno: {s[2]} | Alvo: {s[4]} | Status: {s[3]}"
                )

    elif args.command == "demo":
        _demo(repo_aluno, repo_disc, repo_sol, service)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
