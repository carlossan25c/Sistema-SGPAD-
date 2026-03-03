# main.py
"""
Ponto de entrada da aplicação SGSA — Interface de Linha de Comando (CLI).

Este módulo configura e executa o sistema via argparse, expondo os três
grupos de comandos principais: aluno, disciplina e solicitacao. Cada grupo
suporta subcomandos específicos (cadastrar, listar, remover, criar).

Ao criar solicitações, as regras de negócio correspondentes ao tipo são
aplicadas automaticamente antes de persistir. Qualquer violação é capturada
e exibida ao usuário com uma mensagem clara.
"""

import argparse
import datetime
import time
import sys

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


# Mapeamento de regras padrão por tipo de solicitação.
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
    """Configura e retorna o parser da interface de linha de comando."""
    parser = argparse.ArgumentParser(
        description="SGSA - Sistema de Gestão Académica (Versão JSON)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Comandos principais")

    # ---- Grupo: aluno ----
    aluno_p = subparsers.add_parser("aluno", help="Gestão de alunos")
    aluno_sub = aluno_p.add_subparsers(dest="subcommand")

    cad = aluno_sub.add_parser("cadastrar", help="Cadastrar novo aluno")
    cad.add_argument("--nome", required=True, help="Nome completo do aluno")
    cad.add_argument("--email", required=True, help="E-mail institucional")
    cad.add_argument("--mat", required=True, help="Código de matrícula único")
    cad.add_argument("--curso", required=True, help="Nome do curso")

    aluno_sub.add_parser("listar", help="Listar todos os alunos cadastrados")

    rem = aluno_sub.add_parser("remover", help="Remover aluno pelo código de matrícula")
    rem.add_argument("--mat", required=True, help="Código de matrícula a remover")

    # ---- Grupo: disciplina ----
    disc_p = subparsers.add_parser("disciplina", help="Gestão de disciplinas")
    disc_sub = disc_p.add_subparsers(dest="subcommand")

    cad_d = disc_sub.add_parser("cadastrar", help="Cadastrar nova disciplina")
    cad_d.add_argument("--nome", required=True, help="Nome da disciplina")
    cad_d.add_argument("--carga", type=int, required=True,
                       help="Carga horária em horas (ex: 72)")

    disc_sub.add_parser("listar", help="Listar todas as disciplinas cadastradas")

    # ---- Grupo: solicitacao ----
    sol_p = subparsers.add_parser("solicitacao", help="Gestão de solicitações")
    sol_sub = sol_p.add_subparsers(dest="subcommand")

    criar = sol_sub.add_parser("criar", help="Criar e validar nova solicitação")
    criar.add_argument(
        "--tipo",
        choices=["matricula", "trancamento", "colacao"],
        required=True,
        help="Tipo da solicitação"
    )
    criar.add_argument("--mat", required=True, help="Matrícula do aluno solicitante")
    criar.add_argument("--alvo", required=True,
                       help="Nome da disciplina (matrícula/trancamento) "
                            "ou do curso (colação)")
    criar.add_argument(
        "--prazo",
        default=None,
        help="Prazo do calendário acadêmico no formato YYYY-MM-DD "
             "(obrigatório para trancamento com verificação de prazo)"
    )

    sol_sub.add_parser("listar", help="Listar todas as solicitações registradas")

    return parser


def buscar_disciplina_por_nome(repo_disc, nome: str):
    """Busca uma disciplina no repositório pelo nome."""
    for d in repo_disc.listar():
        if d[0].lower() == nome.lower():
            return Disciplina(nome=d[0], carga_horaria=d[1])
    return None


def exibir_barra_progresso(duracao: int = 3, mensagem: str = "Processando"):
    """Exibe uma barra de progresso animada no terminal."""
    passos = 30
    tempo_por_passo = duracao / passos
    
    print(f"\n⏳ {mensagem}...")
    for i in range(passos + 1):
        porcentagem = (i / passos) * 100
        barra = "█" * i + "░" * (passos - i)
        sys.stdout.write(f"\r[{barra}] {porcentagem:.0f}%")
        sys.stdout.flush()
        time.sleep(tempo_por_passo)
    
    print("\n")


def simular_fluxo_solicitacao(sol, service, repo_sol, tipo: str):
    """Simula o fluxo de processamento com transição de estados."""
    print(f"\n📋 Status inicial: {sol.status}")
    
    exibir_barra_progresso(duracao=3, mensagem="Analisando solicitação no setor acadêmico")
    
    try:
        sol.avancar()
        print(f"✅ Status atualizado: {sol.status}")
        
        exibir_barra_progresso(duracao=2, mensagem="Finalizando análise")
        
        sol.avancar()
        print(f"✅ Status atualizado: {sol.status}")
        
    except Exception as e:
        print(f"⚠️ Não foi possível avançar o estado: {e}")
        return
    
    repo_sol.adicionar(sol, tipo)
    print(f"\n✅ Solicitação de '{tipo}' registrada com status final: {sol.status}")


def main() -> None:
    """Função principal que inicializa o sistema e executa o comando."""
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
            aluno = Aluno(args.nome, args.email, args.mat, Curso(args.curso))
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
            repo_disc.adicionar(Disciplina(args.nome, args.carga))
            print(f"✅ Disciplina '{args.nome}' adicionada.")
        elif args.subcommand == "listar":
            print("\n📚 Lista de Disciplinas:")
            for d in repo_disc.listar():
                print(f"  - {d[0]} ({d[1]}h)")

    elif args.command == "solicitacao":
        if args.subcommand == "criar":
            aluno_obj = Aluno("Estudante", "email@sgsa.com", args.mat, Curso("Geral"))

            alvo_obj = None
            if args.tipo in ["matricula", "trancamento"]:
                alvo_obj = buscar_disciplina_por_nome(repo_disc, args.alvo)
                if not alvo_obj:
                    print(f"❌ Disciplina '{args.alvo}' não encontrada no catálogo.")
                    return
            elif args.tipo == "colacao":
                alvo_obj = Curso(args.alvo)

            kwargs = {}
            if args.tipo == "trancamento" and args.prazo:
                kwargs["prazo"] = datetime.date.fromisoformat(args.prazo)

            try:
                sol = service.criar_solicitacao(args.tipo, aluno_obj, alvo_obj, **kwargs)
                regras = REGRAS_POR_TIPO.get(args.tipo, [])
                service.aplicar_regras(sol, regras)
                
                simular_fluxo_solicitacao(sol, service, repo_sol, args.tipo)
                
            except ViolacaoRegraAcademicaError as e:
                print(f"❌ {e}")

        elif args.subcommand == "listar":
            print("\n📄 Lista de Solicitações:")
            for s in repo_sol.listar():
                print(
                    f"  ID: {s[0]} | Tipo: {s[1]} | "
                    f"Aluno: {s[2]} | Alvo: {s[4]} | Status: {s[3]}"
                )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
