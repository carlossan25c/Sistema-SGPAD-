class NotificacaoService:
    """
    Serviço responsável por gerenciar o envio de alertas e comunicações.
    Funciona como o 'Observer' no ciclo de vida das solicitações.
    """
    def notificar_setor(self, solicitacao):
        """Notifica o setor responsável via console (simulação)."""
        print(f"Notificação enviada para setor responsável pela solicitação de {solicitacao.aluno.nome}")
