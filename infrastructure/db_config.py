# infrastructure/db_config.py
"""
Módulo de configuração e acesso ao banco de dados JSON do SGSA.

Este módulo implementa a persistência simples do sistema utilizando
um arquivo JSON local (sgsa.json) como banco de dados. Toda a lógica
de leitura, escrita e inicialização do arquivo é centralizada aqui,
seguindo o princípio SRP — os repositórios chamam estas funções sem
precisar saber como o armazenamento funciona internamente.

Funções disponíveis:
    - init_db(): cria o arquivo com estrutura inicial se não existir.
    - load_db(): lê e retorna todos os dados do arquivo.
    - save_db(data): sobrescreve o arquivo com os dados fornecidos.
"""

import json
import os

DB_FILE = "sgsa.json"


def init_db() -> None:
    """
    Inicializa o arquivo JSON de persistência com a estrutura básica.

    Verifica se o arquivo sgsa.json já existe no diretório de execução.
    Se não existir, cria-o com as coleções vazias necessárias para o
    funcionamento do sistema: alunos, disciplinas e solicitacoes.

    Deve ser chamada obrigatoriamente no início da execução (main.py)
    para garantir que o arquivo existe antes de qualquer operação de
    leitura ou escrita.

    Efeito colateral:
        Cria o arquivo sgsa.json no diretório de trabalho atual, se
        ainda não existir. Exibe mensagem de confirmação no console.

    Exemplo:
        >>> init_db()
        ✅ Ficheiro sgsa.json criado com sucesso.
        # (ou silêncio, se o arquivo já existia)
    """
    if not os.path.exists(DB_FILE):
        estrutura = {
            "alunos": [],
            "disciplinas": [],
            "solicitacoes": []
        }
        save_db(estrutura)
        print(f"✅ Ficheiro {DB_FILE} criado com sucesso.")


def load_db() -> dict:
    """
    Lê todos os dados do arquivo JSON e retorna como dicionário Python.

    Se o arquivo não existir, chama init_db() automaticamente antes
    de tentar a leitura, garantindo que a operação nunca falhe por
    ausência do arquivo.

    O arquivo é lido com encoding UTF-8 para suporte a caracteres
    especiais (acentos, cedilha, etc.) presentes nos nomes de alunos
    e disciplinas.

    :return: Dicionário com as chaves 'alunos', 'disciplinas' e
             'solicitacoes', cada uma contendo uma lista de registros.
    :raises json.JSONDecodeError: se o arquivo existir mas estiver
                                  corrompido ou com formato inválido.
    """
    if not os.path.exists(DB_FILE):
        init_db()
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_db(data: dict) -> None:
    """
    Persiste os dados fornecidos no arquivo JSON, sobrescrevendo o conteúdo.

    Utiliza indent=4 para manter o arquivo legível por humanos, e
    ensure_ascii=False para preservar caracteres especiais sem
    codificação de escape unicode (ex: 'João' em vez de 'Jo\\u00e3o').

    Atenção: Esta função sobrescreve TODO o conteúdo do arquivo. Para
    atualizações parciais, use load_db(), modifique o dicionário e
    chame save_db() com o dicionário completo.

    :param data: Dicionário completo com todos os dados a serem salvos.
                 Deve conter as chaves 'alunos', 'disciplinas' e
                 'solicitacoes'.
    """
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
