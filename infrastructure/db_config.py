import sqlite3

DB_NAME = "sgsa.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Tabela de alunos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        matricula TEXT NOT NULL,
        curso TEXT NOT NULL
    )
    """)

    # Tabela de solicitações
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS solicitacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,
        aluno_id INTEGER NOT NULL,
        status TEXT NOT NULL,
        disciplina TEXT,
        curso TEXT,
        FOREIGN KEY(aluno_id) REFERENCES alunos(id)
    )
    """)

    conn.commit()
    conn.close()
