# infrastructure/db_config.py
import json
import os

DB_FILE = "sgsa.json"

def init_db():
    """Inicializa o ficheiro JSON com a estrutura básica se não existir."""
    if not os.path.exists(DB_FILE):
        estrutura = {
            "alunos": [],
            "disciplinas": [],
            "solicitacoes": []
        }
        save_db(estrutura)
        print(f"✅ Ficheiro {DB_FILE} criado com sucesso.")

def load_db():
    """Lê todos os dados do ficheiro JSON."""
    if not os.path.exists(DB_FILE):
        init_db()
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    """Guarda os dados fornecidos no ficheiro JSON."""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)