from application.solicitacao_service import SolicitacaoService
from rules.regra_prazo import RegraPrazo
from rules.regra_elegibilidade import RegraElegibilidade
from domain.aluno import Aluno
from domain.curso import Curso
from domain.disciplina import Disciplina
from infrastructure.db_config import init_db, get_connection
from infrastructure.repositorio_aluno import RepositorioAluno
from infrastructure.repositorio_solicitacao import RepositorioSolicitacao
from infrastructure.repositorio_disciplina import RepositorioDisciplina

def menu():
    print("\n=== SISTEMA DE GESTÃO DE SOLICITAÇÕES ACADÊMICAS ===")
    print("[1] Cadastrar aluno")
    print("[2] Solicitar matrícula")
    print("[3] Solicitar trancamento")
    print("[4] Solicitar colação de grau")
    print("[5] Listar alunos")
    print("[6] Listar solicitações")
    print("[7] Cadastrar disciplina")
    print("[8] Listar disciplinas")
    print("[9] Excluir aluno por matrícula")   # nova opção
    print("[0] Sair")

def excluir_aluno_por_matricula(matricula):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alunos WHERE matricula = ?", (matricula,))
    conn.commit()
    conn.close()
    print(f"✅ Aluno com matrícula {matricula} foi removido do banco de dados.")

def main():
    init_db()
    repo_aluno = RepositorioAluno()
    repo_solicitacao = RepositorioSolicitacao()
    repo_disciplina = RepositorioDisciplina()
    service = SolicitacaoService()

    curso_padrao = Curso("Engenharia de Software")

    while True:
        menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "":
            print("⚠️ Você precisa digitar uma opção.")
            continue

        if opcao == "1":
            nome = input("Nome do aluno: ")
            email = input("Email: ")
            matricula = input("Matrícula: ")
            aluno = Aluno(nome, email, matricula, curso_padrao)
            repo_aluno.adicionar(aluno)
            print("✅ Aluno cadastrado com sucesso!")

        elif opcao == "2":
            matricula = input("Informe a matrícula do aluno: ")
            alunos = repo_aluno.listar()
            dados_aluno = next((a for a in alunos if a[2] == matricula), None)
            if dados_aluno:
                nome, email, matricula, curso_nome = dados_aluno
                curso = Curso(curso_nome)
                aluno_obj = Aluno(nome, email, matricula, curso)

                # Escolher disciplina já cadastrada
                print("\n📖 Disciplinas disponíveis:")
                disciplinas = repo_disciplina.listar()
                if not disciplinas:
                    print("⚠️ Nenhuma disciplina cadastrada. Cadastre primeiro em [7].")
                    continue

                for i, d in enumerate(disciplinas, start=1):
                    print(f"[{i}] {d[0]} ({d[1]}h)")

                try:
                    escolha = int(input("Escolha o número da disciplina: "))
                    nome_disc, carga = disciplinas[escolha - 1]
                    disciplina = Disciplina(nome_disc, carga)
                except (ValueError, IndexError):
                    print("⚠️ Escolha inválida.")
                    continue

                solicitacao = service.criar_solicitacao("matricula", aluno_obj, disciplina)
                valido = service.aplicar_regras(solicitacao, [RegraPrazo(), RegraElegibilidade()])
                repo_solicitacao.adicionar(solicitacao, "matricula")

                print("✅ Solicitação criada:", "Aprovada" if valido else "Rejeitada")
            else:
                print("⚠️ Aluno não encontrado.")

        elif opcao == "3":
            print("⚠️ Fluxo de trancamento ainda não implementado.")

        elif opcao == "4":
            print("⚠️ Fluxo de colação de grau ainda não implementado.")

        elif opcao == "5":
            print("\n📚 Alunos cadastrados:")
            alunos = repo_aluno.listar()
            if not alunos:
                print("⚠️ Nenhum aluno cadastrado.")
            else:
                for aluno in alunos:
                    print(f" - Nome: {aluno[0]} | Email: {aluno[1]} | Matrícula: {aluno[2]} | Curso: {aluno[3]}")

        elif opcao == "6":
            print("\n📝 Solicitações registradas:")
            solicitacoes = repo_solicitacao.listar()
            if not solicitacoes:
                print("⚠️ Nenhuma solicitação registrada.")
            else:
                for solicitacao in solicitacoes:
                    print(f" - ID: {solicitacao[0]} | Tipo: {solicitacao[1]} | Status: {solicitacao[3]} | Disciplina: {solicitacao[4]}")

        elif opcao == "7":
            nome_disc = input("Nome da disciplina: ")
            carga = int(input("Carga horária: "))
            disciplina = Disciplina(nome_disc, carga)
            repo_disciplina.adicionar(disciplina)
            print("✅ Disciplina cadastrada com sucesso!")

        elif opcao == "8":
            print("\n📖 Disciplinas disponíveis:")
            disciplinas = repo_disciplina.listar()
            if not disciplinas:
                print("⚠️ Nenhuma disciplina cadastrada.")
            else:
                for disciplina in disciplinas:
                    print(f" - {disciplina[0]} ({disciplina[1]}h)")

        elif opcao == "9":
            matricula = input("Informe a matrícula do aluno a excluir: ")
            excluir_aluno_por_matricula(matricula)

        elif opcao == "0":
            print("👋 Saindo do sistema...")
            break

        else:
            print("⚠️ Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()
