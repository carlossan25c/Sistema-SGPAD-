class NotificacaoService:
    def notificar_setor(self, solicitacao):
        print(f"Notificação enviada para setor responsável pela solicitação de {solicitacao.aluno.nome}")
