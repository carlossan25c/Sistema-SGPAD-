# rules/regra_base.py
"""
Módulo que define a interface abstrata para todas as regras acadêmicas.

Este módulo é o coração do padrão Strategy no SGSA. Ao definir um contrato
único (o método validar), ele permite que novas regras sejam adicionadas
simplesmente criando novas subclasses — sem modificar o SolicitacaoService
nem qualquer outra parte do sistema (OCP).
"""

from abc import ABC, abstractmethod


class Regra(ABC):
    """
    Interface abstrata (Strategy) que define o contrato para todas
    as regras acadêmicas do sistema SGSA.

    Cada regra encapsula um único critério de validação específico
    (pré-requisito, prazo, elegibilidade, etc.) e o expõe através
    do método validar(). O SolicitacaoService recebe uma lista de
    objetos Regra e os chama polimorficamente — sem saber qual regra
    está executando, apenas que cada uma responde ao mesmo método.

    Padrão aplicado: Strategy (GoF).

    Princípios SOLID:
        - SRP: cada subclasse de Regra valida exatamente um critério.
        - OCP: novas regras são adicionadas por criação de subclasses,
               sem alterar código existente.
        - LSP: todas as subclasses respeitam o contrato do método validar().
        - DIP: SolicitacaoService depende desta abstração, não das
               implementações concretas.

    Convenção de implementação:
        O método validar() deve:
          - Retornar True se a regra for satisfeita.
          - Lançar ViolacaoRegraAcademicaError com mensagem clara se falhar.
          - NUNCA retornar False silenciosamente.

    Exemplo de implementação:
        >>> class MinhaRegra(Regra):
        ...     def validar(self, solicitacao) -> bool:
        ...         if not condicao:
        ...             raise ViolacaoRegraAcademicaError(
        ...                 mensagem="Descrição do problema.",
        ...                 regra="MinhaRegra"
        ...             )
        ...         return True
    """

    @abstractmethod
    def validar(self, solicitacao) -> bool:
        """
        Valida a solicitação contra o critério encapsulado por esta regra.

        :param solicitacao: Objeto do tipo Solicitacao (ou subclasse)
                            a ser analisado. A regra acessa os dados
                            necessários a partir deste objeto
                            (aluno, disciplina, curso, etc.).
        :raises ViolacaoRegraAcademicaError: se o critério da regra
                                             não for atendido. A mensagem
                                             deve ser clara e orientar
                                             o usuário sobre o problema.
        :return: True se a solicitação satisfaz os requisitos da regra.
        """
