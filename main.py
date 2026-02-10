from application.solicitacao_service import SolicitacaoService
from rules.regra_prazo import RegraPrazo
from rules.regra_elegibilidade import RegraElegibilidade
from domain.aluno import Aluno
from domain.curso import Curso
from domain.disciplina import Disciplina
from infrastructure.db_config import init_db
from infrastructure.repositorio_aluno import RepositorioAluno
from infrastructure.repositorio_solicitacao import RepositorioSolicitacao

def executar_fluxo():
    # Inicializa o banco
    init_db()

    # Repositórios
    repo_aluno = RepositorioAluno()
    repo_solicitacao = RepositorioSolicitacao()

    # Criar curso e aluno
    curso = Curso("Engenharia de Software")
    aluno = Aluno("Carlos", "carlos@email.com", "2026001", curso)
    repo_aluno.adicionar(aluno)

    # Serviço
    service = SolicitacaoService()

    # Exemplo de solicitação de matrícula
    disciplina = Disciplina("POO", 60)
    solicitacao = service.criar_solicitacao("matricula", aluno, disciplina)
    valido = service.aplicar_regras(solicitacao, [RegraPrazo(), RegraElegibilidade()])
    repo_solicitacao.adicionar(solicitacao, "matricula")

    # Retorna dados estruturados
    return {
        "alunos": repo_aluno.listar(),
        "solicitacoes": repo_solicitacao.listar(),
        "resultado": "Aprovada" if valido else "Rejeitada"
    }

if __name__ == "__main__":
    dados = executar_fluxo()
    # Aqui você decide como exibir (CLI, web, GUI)
    # Exemplo CLI:
    for aluno in dados["alunos"]:
        print("Aluno:", aluno)
    for solicitacao in dados["solicitacoes"]:
        print("Solicitação:", solicitacao)
    print("Resultado final:", dados["resultado"])
