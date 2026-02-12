import sqlite3

def get_connection():
    return sqlite3.connect("sgsa.db")

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Tabela de alunos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            nome TEXT,
            email TEXT,
            matricula TEXT PRIMARY KEY,
            curso TEXT
        )
    """)

    # Tabela de solicitações
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS solicitacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            aluno_id TEXT,
            status TEXT,
            disciplina TEXT,
            curso TEXT
        )
    """)

    # Tabela de disciplinas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS disciplinas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            carga_horaria INTEGER
        )
    """)

    conn.commit()
    conn.close()
