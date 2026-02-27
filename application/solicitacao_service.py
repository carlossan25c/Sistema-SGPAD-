# application/solicitacao_service.py
"""
Módulo que implementa o serviço central de orquestração de solicitações.

O SolicitacaoService é o ponto de entrada da camada de aplicação. Ele
combina três padrões de projeto para fornecer uma interface clara e
extensível: Factory (criação), Strategy (validação) e Observer (notificação).
"""

from domain.solicitacao_trancamento import SolicitacaoTrancamento
from domain.solicitacao_matricula import SolicitacaoMatricula
from domain.solicitacao_colacao import SolicitacaoColacao
from domain.excecoes import ViolacaoRegraAcademicaError


class SolicitacaoService:
    """
    Serviço central que orquestra a criação, validação e processamento
    de solicitações acadêmicas.

    Este serviço é o coração da camada de aplicação e concentra a
    coordenação entre os padrões de projeto do sistema:

    Padrões aplicados:
        Factory Method:
            O método criar_solicitacao() decide qual subclasse concreta
            de Solicitacao instanciar com base no parâmetro 'tipo'. Isso
            isola o código cliente da criação direta de objetos.

        Strategy:
            O método aplicar_regras() recebe uma lista de objetos Regra
            e os chama polimorficamente. O serviço não sabe — nem precisa
            saber — qual regra está sendo executada; ele apenas invoca
            validar() em cada uma. Novas regras são adicionadas sem
            alterar este serviço (OCP).

        Observer:
            O NotificacaoService é injetado no construtor e registrado
            como observador de cada solicitação criada. Isso garante que
            notificações sejam disparadas automaticamente a cada mudança
            de estado, sem acoplamento direto com Solicitacao.

    Princípios SOLID:
        - SRP: responsabilidade única de orquestrar o ciclo de vida das
               solicitações.
        - OCP: novos tipos de solicitação e novas regras são adicionados
               por extensão, sem modificar este serviço.
        - DIP: depende das abstrações Regra e NotificacaoService, não das
               implementações concretas.

    Exemplo de uso completo:
        >>> ntf = NotificacaoService()
        >>> svc = SolicitacaoService(notificacao_service=ntf)
        >>>
        >>> sol = svc.criar_solicitacao("matricula", aluno, calc2)
        >>> svc.aplicar_regras(sol, [RegraPreRequisito(), RegraCoRequisito()])
        >>> svc.processar(sol)   # avança para 'Em Análise' + notifica
    """

    def __init__(self, notificacao_service=None):
        """
        Inicializa o serviço com um NotificacaoService opcional.

        A injeção de dependência permite testar o serviço sem notificações
        reais (passando None ou um mock) e facilita a substituição do
        mecanismo de notificação em produção.

        :param notificacao_service: Instância de NotificacaoService a ser
                                    registrada como observador nas solicitações.
                                    Se None, nenhuma notificação será enviada.
        """
        self._notificacao = notificacao_service

    # ------------------------------------------------------------------
    # Factory Method — criação de solicitações
    # ------------------------------------------------------------------

    def criar_solicitacao(self, tipo: str, aluno, alvo, **kwargs):
        """
        Cria e configura a solicitação correta com base no tipo informado.

        Implementa o padrão Factory Method: o chamador informa o tipo
        como string e recebe o objeto correto sem precisar conhecer as
        subclasses concretas. Após a criação:
          - Registra o NotificacaoService como observador (se disponível).
          - Notifica a Coordenação do Curso ao criar uma SolicitacaoMatricula
            (regra de negócio 3.A).

        :param tipo: Tipo da solicitação. Valores aceitos:
                     'matricula', 'trancamento', 'colacao'.
        :param aluno: Objeto Aluno solicitante.
        :param alvo: Objeto Disciplina (para matrícula e trancamento)
                     ou Curso (para colação).
        :param kwargs: Parâmetros adicionais repassados ao construtor
                       da subclasse (ex: data=, prazo= para trancamento;
                       disciplinas_co_req_solicitadas= para matrícula).
        :raises ValueError: se o tipo informado não for reconhecido.
        :return: Objeto de solicitação instanciado e configurado.
        """
        if tipo == "trancamento":
            solicitacao = SolicitacaoTrancamento(aluno, alvo, **kwargs)
        elif tipo == "matricula":
            solicitacao = SolicitacaoMatricula(aluno, alvo, **kwargs)
        elif tipo == "colacao":
            solicitacao = SolicitacaoColacao(aluno, alvo, **kwargs)
        else:
            raise ValueError(
                f"Tipo de solicitação inválido: '{tipo}'. "
                "Use 'trancamento', 'matricula' ou 'colacao'."
            )

        # Registra o Observer
        if self._notificacao:
            solicitacao.registrar_observador(self._notificacao)

        # Notifica o setor ao criar matrícula (Observer proativo — regra 3.A)
        if tipo == "matricula" and self._notificacao:
            self._notificacao.notificar_setor(solicitacao)

        return solicitacao

    # ------------------------------------------------------------------
    # Strategy — aplicação de regras acadêmicas
    # ------------------------------------------------------------------

    def aplicar_regras(self, solicitacao, regras: list) -> bool:
        """
        Aplica polimorficamente cada regra da lista à solicitação.

        Itera sobre a lista de objetos Regra e chama validar() em cada um.
        A primeira regra que falhar lançará ViolacaoRegraAcademicaError,
        interrompendo a validação imediatamente e propagando a exceção
        ao chamador com uma mensagem clara.

        O serviço não conhece as regras concretas — apenas depende da
        abstração Regra.validar(). Isso garante total desacoplamento
        (DIP) e extensibilidade (OCP).

        :param solicitacao: Objeto Solicitacao a ser validado.
        :param regras: Lista de objetos que implementam a classe Regra.
                       A ordem importa: as regras são avaliadas em sequência.
        :raises ViolacaoRegraAcademicaError: na primeira regra violada,
                                             com mensagem descritiva.
        :return: True se todas as regras forem satisfeitas.
        """
        for regra in regras:
            regra.validar(solicitacao)
        return True

    # ------------------------------------------------------------------
    # Fluxo de estado — conveniência
    # ------------------------------------------------------------------

    def processar(self, solicitacao, regras: list = None) -> None:
        """
        Valida as regras e avança a solicitação para 'Em Análise'.

        Método de conveniência que combina aplicar_regras() + avancar()
        em uma única chamada. Ideal para fluxos diretos onde a validação
        e o avanço acontecem no mesmo momento.

        Se regras for None ou lista vazia, o avanço ocorre sem validação
        prévia — útil em testes ou em fluxos administrativos onde as
        regras já foram verificadas anteriormente.

        :param solicitacao: Objeto Solicitacao criado pelo Factory.
        :param regras: Lista opcional de objetos Regra a validar antes
                       de avançar o estado. Se None, pula a validação.
        :raises ViolacaoRegraAcademicaError: se alguma regra falhar.
        :raises TransicaoEstadoInvalidaError: se o estado atual não
                                              permitir avanço.
        """
        if regras:
            self.aplicar_regras(solicitacao, regras)
        solicitacao.avancar()
