from domain.aluno import Aluno
from domain.setor import SetorAcademico
from domain.solicitacao import SolicitacaoTrancamento
from domain.regra import RegraPrazo, RegraElegibilidade

from persistence.aluno_repository import AlunoRepository
from persistence.solicitacao_repository import SolicitacaoRepository

def main():
    aluno_repo = AlunoRepository()
    solicitacao_repo = SolicitacaoRepository()

    aluno_repo.criar_tabela()
    solicitacao_repo.criar_tabela()

    aluno = Aluno("20231234", "João Silva", "Engenharia")
    aluno_repo.salvar(aluno)

    setor = SetorAcademico("Secretaria Acadêmica", "Maria Souza")

    solicitacao = SolicitacaoTrancamento(aluno, setor)
    solicitacao.adicionar_regra(RegraPrazo())
    solicitacao.adicionar_regra(RegraElegibilidade())

    solicitacao.executar()
    solicitacao.executar()
    solicitacao.executar()

    solicitacao_repo.salvar(solicitacao)

if __name__ == "__main__":
    main()
