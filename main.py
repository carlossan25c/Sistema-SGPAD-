# main.py
"""
Ponto de entrada da aplicação SGSA — Interface de Linha de Comando (CLI).

Este módulo configura e executa o sistema via argparse, expondo os quatro
grupos de comandos principais: aluno, disciplina, solicitacao e demo.

Ao criar solicitações, as regras de negócio correspondentes ao tipo são
aplicadas automaticamente antes de persistir. Qualquer violação é capturada
e exibida ao usuário com uma mensagem clara, e a solicitação é registrada
com status 'Rejeitada'. Solicitações que passam em todas as regras são
registradas com status 'Aprovada'.

O comando 'demo' executa cenários pré-configurados que demonstram
explicitamente casos de aceite e de negação para cada tipo de solicitação.
"""

import argparse
import datetime
import uuid
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
from rules.regra_creditos import RegraCreditos


# ---------------------------------------------------------------------------
# Mapeamento de regras padrão por tipo de solicitação.
# ---------------------------------------------------------------------------
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
        RegraCreditos(minimo=80),
    ],
}


def gerar_protocolo() -> str:
    """Gera um protocolo único no formato SGSA-XXXXXXXX."""
    return f"SGSA-{uuid.uuid4().hex[:8].upper()}"


def setup_argparse() -> argparse.ArgumentParser:
    """Configura e retorna o parser da interface de linha de comando."""
    parser = argparse.ArgumentParser(
        description="SGSA - Sistema de Gestão Acadêmica (Versão JSON)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Comandos principais")

    # ---- aluno ----
    aluno_p = subparsers.add_parser("aluno", help="Gestão de alunos")
    aluno_sub = aluno_p.add_subparsers(dest="subcommand")

    cad = aluno_sub.add_parser("cadastrar", help="Cadastrar novo aluno")
    cad.add_argument("--nome", required=True, help="Nome completo do aluno")
    cad.add_argument("--email", required=True, help="E-mail institucional")
    cad.add_argument("--mat", required=True, help="Código de matrícula único")
    cad.add_argument("--curso", required=True, help="Nome do curso")
    cad.add_argument("--limite-horas", type=int, default=360,
                     help="Limite de carga horária semestral do curso (padrão: 360h)")
    cad.add_argument("--min-optativas", type=int, default=0,
                     help="Mínimo de horas optativas para colação (padrão: 0h)")

    aluno_sub.add_parser("listar")

    rem = aluno_sub.add_parser("remover")
    rem.add_argument("--mat", required=True)

    # ---- disciplina ----
    disc_p = subparsers.add_parser("disciplina", help="Gestão de disciplinas")
    disc_sub = disc_p.add_subparsers(dest="subcommand")

    cad_d = disc_sub.add_parser("cadastrar", help="Cadastrar nova disciplina")
    cad_d.add_argument("--nome", required=True, help="Nome da disciplina")
    cad_d.add_argument("--carga", type=int, required=True,
                       help="Carga horária em horas (ex: 72)")
    cad_d.add_argument("--pre-req", default=None,
                       help="Nome do pré-requisito (disciplina que deve ser cursada antes)")
    cad_d.add_argument("--co-req", default=None,
                       help="Nome do co-requisito (disciplina que deve ser cursada simultaneamente)")
    cad_d.add_argument("--optativa", action="store_true",
                       help="Marca a disciplina como optativa (padrão: obrigatória)")

    disc_sub.add_parser("listar")

    # ---- solicitacao ----
    sol_p = subparsers.add_parser("solicitacao", help="Gestão de solicitações")
    sol_sub = sol_p.add_subparsers(dest="subcommand")

    criar = sol_sub.add_parser("criar", help="Criar e validar nova solicitação")
    criar.add_argument("--tipo", choices=["matricula", "trancamento", "colacao"], required=True)
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
    criar.add_argument(
        "--carga-atual",
        type=int,
        default=0,
        help="Carga horária já matriculada no semestre atual (para verificação de limite)"
    )

    sol_sub.add_parser("listar")

    # ---- demo ----
    subparsers.add_parser("demo", help="Executa todos os cenários de demonstração automaticamente")

    # ---- Grupo: demo ----
    subparsers.add_parser(
        "demo",
        help="Executa cenários de demonstração (aceite e negação de solicitações)"
    )

    return parser


def reconstruir_disciplina(repo_disc: RepositorioDisciplina, nome: str) -> Disciplina:
    """
    Reconstrói um objeto Disciplina completo a partir do banco de dados,
    incluindo pré-requisitos e co-requisitos.

    :param repo_disc: Instância de RepositorioDisciplina.
    :param nome: Nome da disciplina a reconstruir.
    :return: Objeto Disciplina completo, ou None se não encontrado.
    """
    dados = repo_disc.buscar_por_nome(nome)
    if dados is None:
        return None

    disc = Disciplina(
        nome=dados['nome'],
        carga_horaria=dados['carga_horaria'],
        obrigatoria=dados.get('obrigatoria', True)
    )

    # Reconstrói pré-requisitos
    for pre_nome in dados.get('pre_requisitos', []):
        pre_dados = repo_disc.buscar_por_nome(pre_nome)
        if pre_dados:
            pre_disc = Disciplina(
                nome=pre_dados['nome'],
                carga_horaria=pre_dados['carga_horaria'],
                obrigatoria=pre_dados.get('obrigatoria', True)
            )
            disc.adicionar_pre_requisito(pre_disc)

    # Reconstrói co-requisitos
    for co_nome in dados.get('co_requisitos', []):
        co_dados = repo_disc.buscar_por_nome(co_nome)
        if co_dados:
            co_disc = Disciplina(
                nome=co_dados['nome'],
                carga_horaria=co_dados['carga_horaria'],
                obrigatoria=co_dados.get('obrigatoria', True)
            )
            disc.adicionar_co_requisito(co_disc)

    return disc


def buscar_disciplina_por_nome(repo_disc: RepositorioDisciplina, nome: str) -> Disciplina:
    """
    Busca uma disciplina no repositório pelo nome, reconstruindo-a
    completamente com pré-requisitos e co-requisitos.

    :param repo_disc: Instância de RepositorioDisciplina.
    :param nome: Nome da disciplina a buscar.
    :return: Objeto Disciplina completo, ou None se não encontrado.
    """
    return reconstruir_disciplina(repo_disc, nome)


def buscar_aluno_por_matricula(repo_aluno: RepositorioAluno, matricula: str) -> Aluno:
    """
    Busca os dados de um aluno no repositório pela matrícula.

    :param repo_aluno: Instância de RepositorioAluno.
    :param matricula: Código de matrícula a buscar.
    :return: Objeto Aluno reconstruído a partir do JSON, ou None se não encontrado.
    """
    for registro in repo_aluno.listar():
        # registro: (nome, email, matricula, curso, limite_horas, min_optativas)
        if registro[2] == matricula:
            limite_horas = registro[4] if len(registro) > 4 else 360
            min_optativas = registro[5] if len(registro) > 5 else 0
            curso = Curso(registro[3],
                          limite_horas_semestrais=limite_horas,
                          min_horas_optativas=min_optativas)
            return Aluno(registro[0], registro[1], registro[2], curso)
    return None


def processar_solicitacao(sol, service, repo_sol, tipo: str, protocolo: str) -> str:
    """
    Aplica o fluxo de estado e persiste a solicitação como aprovada.

    :param sol: Objeto Solicitacao já validado pelas regras.
    :param service: Instância de SolicitacaoService.
    :param repo_sol: Instância de RepositorioSolicitacao.
    :param tipo: Tipo da solicitação.
    :param protocolo: Código de protocolo gerado para esta solicitação.
    :return: Status final ('Aprovada').
    """
    sol.avancar()  # Aberta → Em Análise
    sol.avancar()  # Em Análise → Aprovada
    sol.protocolo = protocolo
    repo_sol.adicionar(sol, tipo)
    return sol.status


def _linha_separadora(char: str = "─", largura: int = 60) -> str:
    """Retorna uma linha separadora formatada."""
    return char * largura


def _cabecalho_cenario(numero: int, titulo: str) -> None:
    """Imprime o cabeçalho de um cenário de demonstração."""
    print(f"\n{'═' * 60}")
    print(f"  CENÁRIO {numero}: {titulo}")
    print('═' * 60)


def _resultado(status: str, motivo: str = "") -> None:
    """Imprime o resultado de um cenário com ícone visual."""
    if status == "Aprovada":
        icone = "✅ APROVADA"
    elif status == "Rejeitada":
        icone = "❌ REJEITADA"
    else:
        icone = f"⚠️  {status.upper()}"

    print(f"\n  Resultado: {icone}")
    if motivo:
        print(f"  Motivo:    {motivo}")
    print("─" * 60)


def executar_demo(repo_sol: RepositorioSolicitacao) -> None:
    """
    Executa cenários de demonstração que mostram claramente quando
    solicitações são ACEITAS e quando são NEGADAS.

    Cenários cobertos:
        1.  Matrícula ACEITA  — sem pré-requisitos, sem co-requisitos.
        2.  Matrícula NEGADA  — pré-requisito não cumprido.
        3.  Matrícula NEGADA  — co-requisito não matriculado simultaneamente.
        4.  Matrícula NEGADA  — limite de carga horária semestral excedido.
        5.  Trancamento ACEITO — vínculo ativo, dentro do prazo.
        6.  Trancamento NEGADO — prazo acadêmico encerrado.
        7.  Trancamento NEGADO — limite de 4 trancamentos atingido.
        8.  Trancamento NEGADO — vínculo já trancado (duplo trancamento).
        9.  Colação ACEITA  — currículo integralizado, sem pendências.
        10. Colação NEGADA  — disciplina obrigatória não concluída.
        11. Colação NEGADA  — pendência documental em aberto.
        12. Colação NEGADA  — créditos insuficientes.
    """
    service = SolicitacaoService(notificacao_service=None)

    print("\n" + "═" * 60)
    print("  DEMONSTRAÇÃO: CASOS DE ACEITE E NEGAÇÃO DE SOLICITAÇÕES")
    print("  Sistema de Gestão de Solicitações Acadêmicas (SGSA)")
    print("═" * 60)

    def _aluno(nome, mat, curso_nome="Eng. Software", limite_horas=360):
        curso = Curso(curso_nome, limite_horas_semestrais=limite_horas)
        return Aluno(nome, f"{mat}@sgsa.edu.br", mat, curso)

    def _disc(nome, carga=72, obrigatoria=True):
        return Disciplina(nome=nome, carga_horaria=carga, obrigatoria=obrigatoria)

    # ===============================================================
    # BLOCO 1 — SOLICITAÇÕES DE MATRÍCULA
    # ===============================================================
    print("\n\n  ► BLOCO 1: SOLICITAÇÕES DE MATRÍCULA\n")

    # Cenário 1: Matrícula ACEITA
    _cabecalho_cenario(1, "Matrícula ACEITA — sem restrições")
    aluno = _aluno("Carlos Mendes", "MAT001")
    disc_poo = _disc("Programação Orientada a Objetos", 60)
    print(f"  Aluno:      {aluno.nome} (mat. {aluno.matricula})")
    print(f"  Disciplina: {disc_poo.nome} ({disc_poo.carga_horaria}h)")
    print(f"  Pré-req.:   nenhum  |  Co-req.: nenhum  |  Carga atual: 0h")
    try:
        sol = service.criar_solicitacao("matricula", aluno, disc_poo)
        service.aplicar_regras(sol, REGRAS_POR_TIPO["matricula"])
        status = processar_solicitacao(sol, service, repo_sol, "matricula", gerar_protocolo())
        _resultado(status)
    except ViolacaoRegraAcademicaError as e:
        _resultado("Rejeitada", str(e))

    # Cenário 2: Matrícula NEGADA — pré-requisito
    _cabecalho_cenario(2, "Matrícula NEGADA — pré-requisito não cumprido")
    aluno2 = _aluno("Fernanda Costa", "MAT002")
    calc1 = _disc("Cálculo I", 72)
    calc2 = _disc("Cálculo II", 72)
    calc2.adicionar_pre_requisito(calc1)
    print(f"  Aluno:      {aluno2.nome} (mat. {aluno2.matricula})")
    print(f"  Disciplina: {calc2.nome} — exige pré-req.: {calc1.nome}")
    print(f"  Histórico:  Cálculo I → NÃO cursado")
    try:
        sol2 = service.criar_solicitacao("matricula", aluno2, calc2)
        service.aplicar_regras(sol2, REGRAS_POR_TIPO["matricula"])
        status = processar_solicitacao(sol2, service, repo_sol, "matricula", gerar_protocolo())
        _resultado(status)
    except ViolacaoRegraAcademicaError as e:
        sol2.avancar(); sol2.rejeitar()
        sol2.protocolo = gerar_protocolo()
        repo_sol.adicionar(sol2, "matricula")
        _resultado("Rejeitada", str(e))

    # Cenário 3: Matrícula NEGADA — co-requisito
    _cabecalho_cenario(3, "Matrícula NEGADA — co-requisito não matriculado simultaneamente")
    aluno3 = _aluno("Lucas Alves", "MAT003")
    teoria = _disc("Física Teórica", 60)
    lab = _disc("Laboratório de Física", 30)
    teoria.adicionar_co_requisito(lab)
    print(f"  Aluno:      {aluno3.nome} (mat. {aluno3.matricula})")
    print(f"  Disciplina: {teoria.nome} — exige co-req. simultâneo: {lab.nome}")
    print(f"  Simultâneas informadas: nenhuma")
    try:
        sol3 = service.criar_solicitacao("matricula", aluno3, teoria)
        service.aplicar_regras(sol3, REGRAS_POR_TIPO["matricula"])
        status = processar_solicitacao(sol3, service, repo_sol, "matricula", gerar_protocolo())
        _resultado(status)
    except ViolacaoRegraAcademicaError as e:
        sol3.avancar(); sol3.rejeitar()
        sol3.protocolo = gerar_protocolo()
        repo_sol.adicionar(sol3, "matricula")
        _resultado("Rejeitada", str(e))

    # Cenário 4: Matrícula NEGADA — carga horária
    _cabecalho_cenario(4, "Matrícula NEGADA — limite de carga horária excedido")
    aluno4 = _aluno("Beatriz Lima", "MAT004", limite_horas=200)
    disc_pesada = _disc("Projeto de Sistemas", 120)
    sol4 = service.criar_solicitacao("matricula", aluno4, disc_pesada)
    sol4.carga_horaria_semestre_atual = 100
    print(f"  Aluno:      {aluno4.nome} (mat. {aluno4.matricula})")
    print(f"  Disciplina: {disc_pesada.nome} ({disc_pesada.carga_horaria}h)")
    print(f"  Limite: {aluno4.curso.limite_horas_semestrais}h  |  "
          f"Atual: {sol4.carga_horaria_semestre_atual}h  |  "
          f"Total seria: {sol4.carga_horaria_semestre_atual + disc_pesada.carga_horaria}h")
    try:
        service.aplicar_regras(sol4, REGRAS_POR_TIPO["matricula"])
        status = processar_solicitacao(sol4, service, repo_sol, "matricula", gerar_protocolo())
        _resultado(status)
    except ViolacaoRegraAcademicaError as e:
        sol4.avancar(); sol4.rejeitar()
        sol4.protocolo = gerar_protocolo()
        repo_sol.adicionar(sol4, "matricula")
        _resultado("Rejeitada", str(e))

    # ===============================================================
    # BLOCO 2 — SOLICITAÇÕES DE TRANCAMENTO
    # ===============================================================
    print("\n\n  ► BLOCO 2: SOLICITAÇÕES DE TRANCAMENTO\n")
    disc_tran = _disc("Banco de Dados", 60)
    prazo_ok = datetime.date.today() + datetime.timedelta(days=30)
    prazo_vencido = datetime.date.today() - datetime.timedelta(days=10)

    # Cenário 5: Trancamento ACEITO
    _cabecalho_cenario(5, "Trancamento ACEITO — dentro do prazo, vínculo ativo")
    aluno5 = _aluno("Roberto Nunes", "TRA001")
    print(f"  Aluno:      {aluno5.nome} (mat. {aluno5.matricula})")
    print(f"  Vínculo:    {aluno5.historico.status_vinculo}  |  "
          f"Trancamentos: {aluno5.historico.trancamentos}/4  |  "
          f"Prazo: {prazo_ok.strftime('%d/%m/%Y')}")
    try:
        sol5 = service.criar_solicitacao(
            "trancamento", aluno5, disc_tran,
            data=datetime.date.today(), prazo=prazo_ok)
        service.aplicar_regras(sol5, REGRAS_POR_TIPO["trancamento"])
        status = processar_solicitacao(sol5, service, repo_sol, "trancamento", gerar_protocolo())
        _resultado(status)
    except ViolacaoRegraAcademicaError as e:
        _resultado("Rejeitada", str(e))

    # Cenário 6: Trancamento NEGADO — prazo encerrado
    _cabecalho_cenario(6, "Trancamento NEGADO — prazo acadêmico encerrado")
    aluno6 = _aluno("Patrícia Souza", "TRA002")
    print(f"  Aluno:      {aluno6.nome} (mat. {aluno6.matricula})")
    print(f"  Data: {datetime.date.today().strftime('%d/%m/%Y')}  |  "
          f"Prazo limite: {prazo_vencido.strftime('%d/%m/%Y')} (vencido há 10 dias)")
    try:
        sol6 = service.criar_solicitacao(
            "trancamento", aluno6, disc_tran,
            data=datetime.date.today(), prazo=prazo_vencido)
        service.aplicar_regras(sol6, REGRAS_POR_TIPO["trancamento"])
        status = processar_solicitacao(sol6, service, repo_sol, "trancamento", gerar_protocolo())
        _resultado(status)
    except ViolacaoRegraAcademicaError as e:
        sol6.avancar(); sol6.rejeitar()
        sol6.protocolo = gerar_protocolo()
        repo_sol.adicionar(sol6, "trancamento")
        _resultado("Rejeitada", str(e))

    # Cenário 7: Trancamento NEGADO — limite atingido
    _cabecalho_cenario(7, "Trancamento NEGADO — limite de 4 trancamentos atingido")
    aluno7 = _aluno("Marcos Vieira", "TRA003")
    aluno7.historico._trancamentos = 4
    print(f"  Aluno:      {aluno7.nome} (mat. {aluno7.matricula})")
    print(f"  Trancamentos realizados: {aluno7.historico.trancamentos}/4 (limite máximo atingido)")
    try:
        sol7 = service.criar_solicitacao(
            "trancamento", aluno7, disc_tran,
            data=datetime.date.today(), prazo=prazo_ok)
        service.aplicar_regras(sol7, REGRAS_POR_TIPO["trancamento"])
        status = processar_solicitacao(sol7, service, repo_sol, "trancamento", gerar_protocolo())
        _resultado(status)
    except ViolacaoRegraAcademicaError as e:
        sol7.avancar(); sol7.rejeitar()
        sol7.protocolo = gerar_protocolo()
        repo_sol.adicionar(sol7, "trancamento")
        _resultado("Rejeitada", str(e))

    # Cenário 8: Trancamento NEGADO — vínculo trancado
    _cabecalho_cenario(8, "Trancamento NEGADO — vínculo já está 'Trancado'")
    aluno8 = _aluno("Juliana Ramos", "TRA004")
    aluno8.historico.status_vinculo = "Trancado"
    print(f"  Aluno:      {aluno8.nome} (mat. {aluno8.matricula})")
    print(f"  Vínculo atual: {aluno8.historico.status_vinculo} "
          f"(duplo trancamento não permitido)")
    try:
        sol8 = service.criar_solicitacao(
            "trancamento", aluno8, disc_tran,
            data=datetime.date.today(), prazo=prazo_ok)
        service.aplicar_regras(sol8, REGRAS_POR_TIPO["trancamento"])
        status = processar_solicitacao(sol8, service, repo_sol, "trancamento", gerar_protocolo())
        _resultado(status)
    except ViolacaoRegraAcademicaError as e:
        sol8.avancar(); sol8.rejeitar()
        sol8.protocolo = gerar_protocolo()
        repo_sol.adicionar(sol8, "trancamento")
        _resultado("Rejeitada", str(e))

    # ===============================================================
    # BLOCO 3 — SOLICITAÇÕES DE COLAÇÃO DE GRAU
    # ===============================================================
    print("\n\n  ► BLOCO 3: SOLICITAÇÕES DE COLAÇÃO DE GRAU\n")

    # Cenário 9: Colação ACEITA
    _cabecalho_cenario(9, "Colação ACEITA — currículo completo, sem pendências")
    curso_ads = Curso("ADS", min_horas_optativas=0)
    tcc = _disc("TCC", 80, obrigatoria=True)
    poo_disc = _disc("POO", 60, obrigatoria=True)
    curso_ads.adicionar_disciplina(tcc)
    curso_ads.adicionar_disciplina(poo_disc)
    aluno9 = Aluno("Aline Ferreira", "aline@sgsa.edu.br", "COL001", curso_ads)
    aluno9.historico.adicionar_disciplina(tcc, 8.5)
    aluno9.historico.adicionar_disciplina(poo_disc, 9.0)
    print(f"  Aluno:      {aluno9.nome} (mat. {aluno9.matricula})")
    print(f"  Disciplinas: TCC (8.5) ✓ | POO (9.0) ✓")
    print(f"  Pendências: nenhuma  |  Créditos: {aluno9.historico.total_creditos()}h")
    try:
        sol9 = service.criar_solicitacao("colacao", aluno9, curso_ads)
        service.aplicar_regras(sol9, REGRAS_POR_TIPO["colacao"])
        status = processar_solicitacao(sol9, service, repo_sol, "colacao", gerar_protocolo())
        _resultado(status)
    except ViolacaoRegraAcademicaError as e:
        _resultado("Rejeitada", str(e))

    # Cenário 10: Colação NEGADA — obrigatória pendente
    _cabecalho_cenario(10, "Colação NEGADA — disciplina obrigatória não concluída")
    curso_si = Curso("Sistemas de Informação", min_horas_optativas=0)
    tcc2 = _disc("TCC", 80, obrigatoria=True)
    etica = _disc("Ética em TI", 40, obrigatoria=True)
    curso_si.adicionar_disciplina(tcc2)
    curso_si.adicionar_disciplina(etica)
    aluno10 = Aluno("Diego Martins", "diego@sgsa.edu.br", "COL002", curso_si)
    aluno10.historico.adicionar_disciplina(tcc2, 7.0)
    # Ética em TI NÃO cursada
    print(f"  Aluno:      {aluno10.nome} (mat. {aluno10.matricula})")
    print(f"  Disciplinas: TCC (7.0) ✓ | Ética em TI → NÃO cursada ✗")
    try:
        sol10 = service.criar_solicitacao("colacao", aluno10, curso_si)
        service.aplicar_regras(sol10, REGRAS_POR_TIPO["colacao"])
        status = processar_solicitacao(sol10, service, repo_sol, "colacao", gerar_protocolo())
        _resultado(status)
    except ViolacaoRegraAcademicaError as e:
        sol10.avancar(); sol10.rejeitar()
        sol10.protocolo = gerar_protocolo()
        repo_sol.adicionar(sol10, "colacao")
        _resultado("Rejeitada", str(e))

    # Cenário 11: Colação NEGADA — pendência documental
    _cabecalho_cenario(11, "Colação NEGADA — pendência documental em aberto")
    curso_cc = Curso("Ciência da Computação", min_horas_optativas=0)
    prog = _disc("Programação I", 72, obrigatoria=True)
    prog2 = _disc("Programação II", 72, obrigatoria=True)
    curso_cc.adicionar_disciplina(prog)
    curso_cc.adicionar_disciplina(prog2)
    aluno11 = Aluno("Renata Gomes", "renata@sgsa.edu.br", "COL003", curso_cc)
    aluno11.historico.adicionar_disciplina(prog, 9.5)
    aluno11.historico.adicionar_disciplina(prog2, 8.0)
    aluno11.adicionar_pendencia("Débito na biblioteca")
    aluno11.adicionar_pendencia("Certidão de nascimento pendente")
    print(f"  Aluno:      {aluno11.nome} (mat. {aluno11.matricula})")
    print(f"  Currículo:  completo ✓")
    print(f"  Pendências: {', '.join(aluno11.pendencias)}")
    try:
        sol11 = service.criar_solicitacao("colacao", aluno11, curso_cc)
        service.aplicar_regras(sol11, REGRAS_POR_TIPO["colacao"])
        status = processar_solicitacao(sol11, service, repo_sol, "colacao", gerar_protocolo())
        _resultado(status)
    except ViolacaoRegraAcademicaError as e:
        sol11.avancar(); sol11.rejeitar()
        sol11.protocolo = gerar_protocolo()
        repo_sol.adicionar(sol11, "colacao")
        _resultado("Rejeitada", str(e))

    # Cenário 12: Colação NEGADA — créditos insuficientes
    _cabecalho_cenario(12, "Colação NEGADA — créditos insuficientes (< 80h)")
    curso_mat = Curso("Matemática", min_horas_optativas=0)
    intro = _disc("Introdução à Matemática", 40, obrigatoria=True)
    curso_mat.adicionar_disciplina(intro)
    aluno12 = Aluno("Pedro Carvalho", "pedro@sgsa.edu.br", "COL004", curso_mat)
    aluno12.historico.adicionar_disciplina(intro, 8.0)
    print(f"  Aluno:      {aluno12.nome} (mat. {aluno12.matricula})")
    print(f"  Créditos: {aluno12.historico.total_creditos()}h  |  Mínimo exigido: 80h")
    try:
        sol12 = service.criar_solicitacao("colacao", aluno12, curso_mat)
        service.aplicar_regras(sol12, REGRAS_POR_TIPO["colacao"])
        status = processar_solicitacao(sol12, service, repo_sol, "colacao", gerar_protocolo())
        _resultado(status)
    except ViolacaoRegraAcademicaError as e:
        sol12.avancar(); sol12.rejeitar()
        sol12.protocolo = gerar_protocolo()
        repo_sol.adicionar(sol12, "colacao")
        _resultado("Rejeitada", str(e))

    # ---------------------------------------------------------------
    # Resumo final
    # ---------------------------------------------------------------
    print("\n" + "═" * 60)
    print("  RESUMO DA DEMONSTRAÇÃO")
    print("═" * 60)
    print(f"  {'Cen.':<6} {'Tipo':<14} {'Resultado'}")
    print("  " + "─" * 56)
    resumo = [
        ("1",  "Matrícula",   "✅ APROVADA  — sem restrições"),
        ("2",  "Matrícula",   "❌ NEGADA    — pré-requisito não cumprido"),
        ("3",  "Matrícula",   "❌ NEGADA    — co-requisito não simultâneo"),
        ("4",  "Matrícula",   "❌ NEGADA    — carga horária excedida"),
        ("5",  "Trancamento", "✅ APROVADA  — dentro do prazo, vínculo ativo"),
        ("6",  "Trancamento", "❌ NEGADA    — prazo encerrado"),
        ("7",  "Trancamento", "❌ NEGADA    — limite de 4 trancamentos"),
        ("8",  "Trancamento", "❌ NEGADA    — vínculo já trancado"),
        ("9",  "Colação",     "✅ APROVADA  — currículo completo"),
        ("10", "Colação",     "❌ NEGADA    — disciplina obrigatória pendente"),
        ("11", "Colação",     "❌ NEGADA    — pendência documental"),
        ("12", "Colação",     "❌ NEGADA    — créditos insuficientes"),
    ]
    for num, tipo, resultado in resumo:
        print(f"  {num:<6} {tipo:<14} {resultado}")
    print("═" * 60 + "\n")


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
            limite_horas = getattr(args, 'limite_horas', 360) or 360
            min_optativas = getattr(args, 'min_optativas', 0) or 0
            curso_obj = Curso(args.curso,
                              limite_horas_semestrais=limite_horas,
                              min_horas_optativas=min_optativas)
            aluno = Aluno(args.nome, args.email, args.mat, curso_obj)
            repo_aluno.adicionar(aluno)
            print(f"✅ Aluno '{args.nome}' cadastrado com sucesso! (UUID: {aluno.id})")
        elif args.subcommand == "listar":
            registros = repo_aluno.listar()
            if not registros:
                print("  Nenhum aluno cadastrado.")
            else:
                print("\n📋 Lista de Alunos:")
                for a in registros:
                    print(f"  - {a[0]} | Mat: {a[2]} | Curso: {a[3]} | E-mail: {a[1]}")
        elif args.subcommand == "remover":
            repo_aluno.remover(args.mat)

    elif args.command == "disciplina":
        if args.subcommand == "cadastrar":
            obrigatoria = not getattr(args, 'optativa', False)
            disc = Disciplina(args.nome, args.carga, obrigatoria=obrigatoria)
            repo_disc.adicionar(disc)

            # Processa pré-requisito se informado
            pre_req_nome = getattr(args, 'pre_req', None)
            if pre_req_nome:
                pre_dados = repo_disc.buscar_por_nome(pre_req_nome)
                if pre_dados:
                    db_pre_reqs = repo_disc.buscar_por_nome(args.nome).get('pre_requisitos', [])
                    if pre_req_nome not in db_pre_reqs:
                        db_pre_reqs.append(pre_req_nome)
                    repo_disc.atualizar_pre_requisitos(args.nome, db_pre_reqs)
                    print(f"   Pré-requisito '{pre_req_nome}' vinculado.")
                else:
                    print(f"   ⚠️  Pré-requisito '{pre_req_nome}' não encontrado no catálogo.")

            # Processa co-requisito se informado
            co_req_nome = getattr(args, 'co_req', None)
            if co_req_nome:
                co_dados = repo_disc.buscar_por_nome(co_req_nome)
                if co_dados:
                    db_co_reqs = repo_disc.buscar_por_nome(args.nome).get('co_requisitos', [])
                    if co_req_nome not in db_co_reqs:
                        db_co_reqs.append(co_req_nome)
                    repo_disc.atualizar_co_requisitos(args.nome, db_co_reqs)
                    print(f"   Co-requisito '{co_req_nome}' vinculado.")
                else:
                    print(f"   ⚠️  Co-requisito '{co_req_nome}' não encontrado no catálogo.")

            print(f"✅ Disciplina '{args.nome}' ({args.carga}h) adicionada.")

        elif args.subcommand == "listar":
            disciplinas = repo_disc.listar_completo()
            if not disciplinas:
                print("  Nenhuma disciplina cadastrada.")
            else:
                print("\n📚 Lista de Disciplinas:")
                for d in disciplinas:
                    tipo = "Obrigatória" if d.get('obrigatoria', True) else "Optativa"
                    pre_reqs = ", ".join(d.get('pre_requisitos', [])) or "nenhum"
                    co_reqs = ", ".join(d.get('co_requisitos', [])) or "nenhum"
                    print(f"  - {d['nome']} ({d['carga_horaria']}h) | {tipo} "
                          f"| Pré-req: {pre_reqs} | Co-req: {co_reqs}")

    elif args.command == "solicitacao":
        if args.subcommand == "criar":
            # Busca o aluno real no banco de dados
            aluno_obj = buscar_aluno_por_matricula(repo_aluno, args.mat)
            if not aluno_obj:
                print(f"❌ Aluno com matrícula '{args.mat}' não encontrado. "
                      f"Cadastre o aluno primeiro com: aluno cadastrar --nome ... --mat {args.mat}")
                return

            alvo_obj = None
            if args.tipo in ["matricula", "trancamento"]:
                # Reconstrói a disciplina com pré/co-requisitos do banco
                alvo_obj = buscar_disciplina_por_nome(repo_disc, args.alvo)
                if not alvo_obj:
                    print(f"❌ Disciplina '{args.alvo}' não encontrada no catálogo.")
                    return
            elif args.tipo == "colacao":
                alvo_obj = aluno_obj.curso  # usa o curso real do aluno

            kwargs = {}
            if args.tipo == "trancamento" and args.prazo:
                kwargs["prazo"] = datetime.date.fromisoformat(args.prazo)
                kwargs["data"] = datetime.date.today()

            protocolo = gerar_protocolo()
            print(f"\n📋 Protocolo: {protocolo}")
            print(f"   Aluno:  {aluno_obj.nome} (mat. {aluno_obj.matricula})")
            print(f"   Tipo:   {args.tipo.capitalize()}")
            alvo_nome = alvo_obj.nome if hasattr(alvo_obj, 'nome') else str(alvo_obj)
            print(f"   Alvo:   {alvo_nome}")

            # Exibe informações de pré/co-requisitos para matrícula
            if args.tipo == "matricula":
                pre_reqs = [p.nome for p in alvo_obj.pre_requisitos]
                co_reqs = [c.nome for c in alvo_obj.co_requisitos]
                if pre_reqs:
                    print(f"   Pré-requisitos: {', '.join(pre_reqs)}")
                if co_reqs:
                    print(f"   Co-requisitos: {', '.join(co_reqs)}")

            try:
                sol = service.criar_solicitacao(args.tipo, aluno_obj, alvo_obj, **kwargs)
                # Aplica carga horária atual se informada (para RegraLimiteCargaHoraria)
                carga_atual = getattr(args, 'carga_atual', 0) or 0
                if carga_atual > 0 and args.tipo == "matricula":
                    sol.carga_horaria_semestre_atual = carga_atual
                regras = REGRAS_POR_TIPO.get(args.tipo, [])
                service.aplicar_regras(sol, regras)

                status = processar_solicitacao(sol, service, repo_sol, args.tipo, protocolo)
                print(f"\n✅ Solicitação {protocolo} APROVADA!")
                print(f"   Status final: {status}")

            except ViolacaoRegraAcademicaError as e:
                print(f"\n❌ Solicitação {protocolo} NEGADA.")
                print(f"   Motivo: {e}")
                try:
                    sol.avancar()
                    sol.rejeitar()
                    sol.protocolo = protocolo
                    repo_sol.adicionar(sol, args.tipo)
                    print(f"   Registro salvo com status: Rejeitada")
                except Exception:
                    pass

        elif args.subcommand == "listar":
            solicitacoes = repo_sol.listar()
            if not solicitacoes:
                print("  Nenhuma solicitação registrada.")
            else:
                print("\n📄 Lista de Solicitações:")
                print(f"  {'ID':<4} {'Protocolo':<16} {'Tipo':<12} "
                      f"{'Aluno':<12} {'Alvo':<30} {'Status'}")
                print("  " + "─" * 90)
                for s in solicitacoes:
                    protocolo_val = s[5] if len(s) > 5 else "S/P"
                    print(
                        f"  {str(s[0]):<4} "
                        f"{str(protocolo_val):<16} "
                        f"{str(s[1]):<12} "
                        f"{str(s[2]):<12} "
                        f"{str(s[4]):<30} "
                        f"{s[3]}"
                    )

    elif args.command == "demo":
        executar_demo(repo_sol)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()