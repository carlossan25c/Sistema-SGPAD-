# application/notificacao_service.py
"""
Módulo que implementa o serviço de notificações do SGSA.

Este serviço funciona como Observador (padrão Observer): é registrado
diretamente nas solicitações e chamado automaticamente a cada mudança
de estado. Centraliza toda a lógica de comunicação do sistema, permitindo
que no futuro os métodos de envio sejam substituídos por integrações reais
(e-mail, SMS, push) sem alterar nenhuma outra parte do sistema.
"""


class NotificacaoService:
    """
    Serviço de notificações que implementa a interface de Observador.

    Este serviço é registrado em Solicitacao via registrar_observador()
    e é chamado automaticamente pelo método _notificar_observadores()
    após cada transição de estado (avancar, cancelar, rejeitar).

    Além de reagir a mudanças de estado (Observer passivo), também pode
    ser chamado diretamente pelo SolicitacaoService para notificações
    proativas — como alertar a Coordenação ao criar uma nova matrícula.

    Padrão aplicado: Observer (GoF).
    Papel neste padrão: ConcreteObserver.

    Princípios SOLID:
        - SRP: responsabilidade única de gerenciar comunicações.
        - OCP: novos canais de notificação (e-mail real, SMS) podem
               ser adicionados sem modificar esta classe — basta criar
               uma subclasse ou injetar um adapter.
        - DIP: Solicitacao depende da abstração (método atualizar()),
               não desta implementação concreta.

    Simulação atual:
        Os métodos de envio são simulados via print() no console.
        Em produção, substituir por chamadas a APIs de e-mail ou
        serviços de mensageria.

    Exemplo de uso:
        >>> ntf = NotificacaoService()
        >>> sol = SolicitacaoMatricula(aluno, disciplina)
        >>> sol.registrar_observador(ntf)
        >>> sol.avancar()
        # [Notificação → Aluno 'João'] Sua solicitação de
        # SolicitacaoMatricula teve o status atualizado para: 'Em Análise'.
    """

    def atualizar(self, solicitacao) -> None:
        """
        Callback chamado automaticamente pela solicitação após cada
        mudança de estado (interface do padrão Observer).

        Este é o ponto de entrada do Observer. Quando a solicitação
        muda de estado, ela chama atualizar() em todos os observadores
        registrados. Aqui, o serviço decide como responder — neste caso,
        notificando o aluno sobre a mudança.

        :param solicitacao: Objeto Solicitacao que teve o estado alterado.
                            Contém aluno, tipo da solicitação e novo status.
        """
        self._notificar_aluno(solicitacao)

    def notificar_setor(self, solicitacao,
                        nome_setor: str = "Coordenação do Curso") -> None:
        """
        Notifica proativamente o setor responsável sobre uma solicitação.

        Chamado explicitamente pelo SolicitacaoService ao criar uma
        SolicitacaoMatricula — regra de negócio 3.A (Observer proativo).
        Permite que a Coordenação seja avisada imediatamente sobre novas
        matrículas sem esperar por uma mudança de estado.

        :param solicitacao: Objeto Solicitacao recém-criado.
        :param nome_setor: Nome do setor a ser notificado.
                           Padrão: 'Coordenação do Curso'.
        """
        print(
            f"[Notificação → Setor '{nome_setor}'] "
            f"Nova solicitação de {solicitacao.__class__.__name__} "
            f"para o aluno '{solicitacao.aluno.nome}' "
            f"(Status: {solicitacao.status})."
        )

    def _notificar_aluno(self, solicitacao) -> None:
        """
        Envia notificação ao aluno sobre a mudança de status.

        Método privado chamado por atualizar(). Simula o envio de um
        e-mail ao aluno informando o novo status da solicitação.

        Em produção, este método deve integrar com um serviço de e-mail
        (ex: SendGrid, SMTP) usando aluno.email como destinatário.

        :param solicitacao: Objeto Solicitacao com dados do aluno e novo status.
        """
        print(
            f"[Notificação → Aluno '{solicitacao.aluno.nome}'] "
            f"Sua solicitação de {solicitacao.__class__.__name__} "
            f"teve o status atualizado para: '{solicitacao.status}'."
        )
