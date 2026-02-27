# infrastructure/repositorio_aluno.py
"""
Módulo que implementa o repositório de persistência de alunos.

Este repositório é responsável por todas as operações de CRUD (Create,
Read, Delete) de alunos no arquivo JSON. Ele isola a camada de domínio
da lógica de persistência, seguindo o princípio da separação de responsabilidades
e o padrão Repository.
"""

from infrastructure.db_config import load_db, save_db


class RepositorioAluno:
    """
    Gerencia a persistência de objetos Aluno no arquivo JSON (sgsa.json).

    Implementa o padrão Repository: fornece uma interface orientada ao
    domínio para operações de persistência, abstraindo completamente
    os detalhes de como os dados são armazenados. O restante do sistema
    nunca acessa o arquivo JSON diretamente — apenas este repositório.

    Padrão aplicado: Repository.

    Princípios SOLID:
        - SRP: responsabilidade única de persistir e recuperar alunos.
        - DIP: a camada de aplicação depende deste repositório (abstração),
               não do mecanismo de persistência (JSON, banco relacional, etc.).

    Nota de serialização:
        Objetos Aluno são convertidos para dicionários simples ao salvar
        (apenas os campos primitivos), pois JSON não suporta objetos Python
        diretamente. O curso é salvo apenas como string (nome).

    Exemplo de uso:
        >>> repo = RepositorioAluno()
        >>> repo.adicionar(aluno)
        >>> for registro in repo.listar():
        ...     print(registro)  # (nome, email, matricula, curso)
    """

    def adicionar(self, aluno) -> None:
        """
        Persiste um novo aluno no arquivo JSON.

        Verifica se já existe um registro com a mesma matrícula antes
        de salvar, evitando duplicatas. Se a matrícula já estiver
        cadastrada, exibe aviso e abandona a operação sem modificar
        o arquivo.

        :param aluno: Objeto Aluno a ser persistido. Os atributos
                      utilizados são: nome, email, matricula, curso.nome.
        """
        db = load_db()
        if any(a['matricula'] == aluno.matricula for a in db['alunos']):
            print(f"⚠️ Erro: Matrícula {aluno.matricula} já existe.")
            return

        db['alunos'].append({
            "nome": aluno.nome,
            "email": aluno.email,
            "matricula": aluno.matricula,
            "curso": aluno.curso.nome
        })
        save_db(db)

    def listar(self) -> list:
        """
        Retorna todos os alunos cadastrados como lista de tuplas.

        Cada tupla contém os campos: (nome, email, matricula, curso).
        Este formato de retorno mantém compatibilidade com o código
        de exibição do main.py.

        :return: Lista de tuplas (nome, email, matricula, curso).
                 Retorna lista vazia se não houver alunos cadastrados.
        """
        db = load_db()
        return [
            (a['nome'], a['email'], a['matricula'], a['curso'])
            for a in db['alunos']
        ]

    def remover(self, matricula: str) -> None:
        """
        Remove o aluno com a matrícula informada do arquivo JSON.

        Filtra a lista de alunos excluindo o registro com a matrícula
        correspondente. Se nenhum registro for encontrado, exibe aviso
        sem lançar exceção.

        :param matricula: Código de matrícula do aluno a ser removido.
        """
        db = load_db()
        original_count = len(db['alunos'])
        db['alunos'] = [a for a in db['alunos'] if a['matricula'] != matricula]

        if len(db['alunos']) < original_count:
            save_db(db)
            print(f"✅ Aluno {matricula} removido.")
        else:
            print(f"⚠️ Aluno com matrícula '{matricula}' não encontrado.")
