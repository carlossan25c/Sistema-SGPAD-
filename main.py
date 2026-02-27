# main.py
"""
Ponto de entrada da aplicação SGSA — Interface de Linha de Comando (CLI).

Este módulo configura e executa o sistema via argparse, expondo os três
grupos de comandos principais: aluno, disciplina e solicitacao. Cada grupo
suporta subcomandos específicos (cadastrar, listar, remover, criar).

Ao criar solicitações, as regras de negócio correspondentes ao tipo são
aplicadas automaticamente antes de persistir. Qualquer violação é capturada
e exibida ao usuário com uma mensagem clara.

Uso básico:
    python main.py aluno cadastrar --nome "João" --email "j@email.com"
                                   --mat "001" --curso "ADS"
    python main.py aluno listar
    python main.py disciplina cadastrar --nome "Cálculo I" --carga 72
    python main.py solicitacao criar --tipo matricula --mat "001"
                                     --alvo "Cálculo I"
    python main.py solicitacao criar --tipo trancamento --mat "001"
                                     --alvo "Cálculo I"
                                     --prazo 2025-10-31
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


# Mapeamento de regras padrão por tipo de solicitação.
# Permite que o main aplique as regras corretas sem precisar conhecer
# os detalhes de cada tipo — basta consultar este dicionário.
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
    """
    Configura e retorna o parser da interface de linha de comando.

    Define a estrutura hierárquica de comandos do SGSA:
      - aluno: cadastrar, listar, remover
      - disciplina: cadastrar, listar
      - solicitacao: criar, listar

    :return: ArgumentParser configurado com todos os subcomandos e
             argumentos necessários.
    """
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


def main() -> None:
    """
    Função principal que inicializa o sistema e executa o comando solicitado.

    Fluxo de execução:
      1. Inicializa o banco de dados JSON (init_db).
      2. Faz o parse dos argumentos de linha de comando.
      3. Instancia os repositórios e serviços necessários.
      4. Executa a ação correspondente ao comando e subcomando informados.
      5. Captura ViolacaoRegraAcademicaError e exibe mensagem amigável.
    """
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

            # Parâmetros extras específicos por tipo
            kwargs = {}
            if args.tipo == "trancamento" and args.prazo:
                kwargs["prazo"] = datetime.date.fromisoformat(args.prazo)

            try:
                sol = service.criar_solicitacao(args.tipo, aluno_obj, args.alvo, **kwargs)
                regras = REGRAS_POR_TIPO.get(args.tipo, [])
                service.aplicar_regras(sol, regras)
                repo_sol.adicionar(sol, args.tipo)
                print(f"✅ Solicitação de '{args.tipo}' registrada e validada.")
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
