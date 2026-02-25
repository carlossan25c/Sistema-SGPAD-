import json
import os

DB_FILE = "sgsa.json"


# =========================
# INICIALIZAÇÃO
# =========================

def init_db():
    """Cria o arquivo JSON se não existir."""
    if not os.path.exists(DB_FILE):
        estrutura = {
            "alunos": [],
            "disciplinas": [],
            "solicitacoes": []
        }
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(estrutura, f, indent=4)


def load_db():
    """Carrega os dados do JSON."""
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_db(data):
    """Salva os dados no JSON."""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def gerar_id(lista):
    """Simula AUTO_INCREMENT."""
    if not lista:
        return 1
    return max(item["id"] for item in lista) + 1


# =========================
# CRUD ALUNOS
# =========================

def adicionar_aluno(nome, email, matricula, curso):
    db = load_db()

    # Verifica PRIMARY KEY (matricula)
    for aluno in db["alunos"]:
        if aluno["matricula"] == matricula:
            print("Erro: Matrícula já cadastrada.")
            return False

    novo_aluno = {
        "nome": nome,
        "email": email,
        "matricula": matricula,
        "curso": curso
    }

    db["alunos"].append(novo_aluno)
    save_db(db)
    return True


def listar_alunos():
    db = load_db()
    return db["alunos"]


def buscar_aluno(matricula):
    db = load_db()
    for aluno in db["alunos"]:
        if aluno["matricula"] == matricula:
            return aluno
    return None


def remover_aluno(matricula):
    db = load_db()
    db["alunos"] = [
        aluno for aluno in db["alunos"]
        if aluno["matricula"] != matricula
    ]
    save_db(db)


# =========================
# CRUD DISCIPLINAS
# =========================

def adicionar_disciplina(nome, carga_horaria):
    db = load_db()

    novo_id = gerar_id(db["disciplinas"])

    nova_disciplina = {
        "id": novo_id,
        "nome": nome,
        "carga_horaria": carga_horaria
    }

    db["disciplinas"].append(nova_disciplina)
    save_db(db)
    return novo_id


def listar_disciplinas():
    db = load_db()
    return db["disciplinas"]


def buscar_disciplina(disciplina_id):
    db = load_db()
    for disciplina in db["disciplinas"]:
        if disciplina["id"] == disciplina_id:
            return disciplina
    return None


def remover_disciplina(disciplina_id):
    db = load_db()
    db["disciplinas"] = [
        d for d in db["disciplinas"]
        if d["id"] != disciplina_id
    ]
    save_db(db)


# =========================
# CRUD SOLICITAÇÕES
# =========================

def adicionar_solicitacao(tipo, aluno_id, disciplina, curso):
    db = load_db()

    # Verifica se aluno existe (simulando integridade referencial)
    aluno = buscar_aluno(aluno_id)
    if not aluno:
        print("Erro: Aluno não encontrado.")
        return False

    novo_id = gerar_id(db["solicitacoes"])

    nova_solicitacao = {
        "id": novo_id,
        "tipo": tipo,
        "aluno_id": aluno_id,
        "status": "Pendente",
        "disciplina": disciplina,
        "curso": curso
    }

    db["solicitacoes"].append(nova_solicitacao)
    save_db(db)
    return True


def listar_solicitacoes():
    db = load_db()
    return db["solicitacoes"]


def atualizar_status_solicitacao(solicitacao_id, novo_status):
    db = load_db()

    for solicitacao in db["solicitacoes"]:
        if solicitacao["id"] == solicitacao_id:
            solicitacao["status"] = novo_status
            save_db(db)
            return True

    print("Solicitação não encontrada.")
    return False


def remover_solicitacao(solicitacao_id):
    db = load_db()
    db["solicitacoes"] = [
        s for s in db["solicitacoes"]
        if s["id"] != solicitacao_id
    ]
    save_db(db)