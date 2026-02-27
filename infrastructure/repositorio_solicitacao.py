# infrastructure/repositorio_solicitacao.py
"""
Módulo que implementa o repositório de persistência de solicitações.

Gerencia o armazenamento de solicitações acadêmicas no arquivo JSON,
extraindo os dados relevantes dos objetos de domínio e convertendo-os
para um formato serializável.
"""

from infrastructure.db_config import load_db, save_db


class RepositorioSolicitacao:
    """
    Gerencia a persistência de objetos Solicitacao no arquivo JSON.

    Realiza a serialização dos objetos de domínio para registros JSON,
    extraindo de forma segura os campos relevantes: tipo, aluno, status
    e o 'alvo' (disciplina ou curso relacionado à solicitação).

    Padrão aplicado: Repository.

    Princípios SOLID:
        - SRP: responsabilidade única de persistir e recuperar solicitações.

    Estratégia de extração do 'alvo':
        A solicitação pode ter uma disciplina ou um curso como alvo.
        O repositório usa getattr() para tentar obter um ou outro de
        forma segura, e extrai o nome do objeto se ele existir. Se
        nenhum alvo estiver presente, usa 'N/A'.

    Nota sobre IDs:
        O ID é gerado como len(lista) + 1 no momento da inserção.
        Este método simples não garante unicidade em caso de exclusões,
        mas é adequado para o escopo atual do sistema.

    Exemplo de uso:
        >>> repo = RepositorioSolicitacao()
        >>> repo.adicionar(solicitacao, "matricula")
        ✅ Solicitação S/P guardada com sucesso.
        >>> for s in repo.listar():
        ...     print(s)  # (id, tipo, aluno_id, status, alvo)
    """

    def adicionar(self, solicitacao, tipo: str) -> None:
        """
        Persiste uma solicitação no arquivo JSON.

        Serializa os dados essenciais da solicitação de domínio para
        um dicionário JSON. O campo 'alvo' é extraído de forma segura:
        tenta obter disciplina ou curso e, se encontrado, usa o nome;
        caso contrário, registra 'N/A'.

        :param solicitacao: Objeto Solicitacao (ou subclasse) a persistir.
        :param tipo: String descrevendo o tipo da solicitação
                     ('matricula', 'trancamento' ou 'colacao').
                     Armazenado explicitamente pois não é possível
                     inferir o tipo apenas do objeto JSON.
        """
        db = load_db()

        if 'solicitacoes' not in db:
            db['solicitacoes'] = []

        # Extração segura do alvo (disciplina ou curso)
        alvo_obj = getattr(solicitacao, 'disciplina', None) or \
                   getattr(solicitacao, 'curso', None)
        if alvo_obj:
            alvo_nome = alvo_obj.nome if hasattr(alvo_obj, 'nome') else str(alvo_obj)
        else:
            alvo_nome = "N/A"

        nova_sol = {
            "id": len(db['solicitacoes']) + 1,
            "protocolo": getattr(solicitacao, 'protocolo', "S/P"),
            "tipo": tipo,
            "aluno_id": solicitacao.aluno.matricula,
            "status": solicitacao.status,
            "alvo": alvo_nome
        }

        db['solicitacoes'].append(nova_sol)
        save_db(db)
        print(f"✅ Solicitação {nova_sol['protocolo']} guardada com sucesso.")

    def listar(self) -> list:
        """
        Retorna todas as solicitações persistidas como lista de tuplas.

        Cada tupla contém: (id, tipo, aluno_id, status, alvo).
        Usa dict.get() com None como fallback para tolerar registros
        incompletos no arquivo (compatibilidade retroativa).

        :return: Lista de tuplas (id, tipo, aluno_id, status, alvo).
                 Retorna lista vazia se não houver solicitações.
        """
        db = load_db()
        return [
            (
                s.get('id'),
                s.get('tipo'),
                s.get('aluno_id'),
                s.get('status'),
                s.get('alvo')
            )
            for s in db.get('solicitacoes', [])
        ]
