class MissionSystem:
    def __init__(self, player, log_callback):
        self.player = player
        self.log_mensagem = log_callback
        self.missoes = {
            'matar_goblins': {'objetivo': 'Mate 3 Goblins', 'quantidade': 0, 'alvo': 3, 'recompensa': 50, 'completa': False},
            'coletar_ouro': {'objetivo': 'Colete 100 de ouro', 'quantidade': 0, 'alvo': 100, 'recompensa': 30, 'completa': False}
        }

    def atualizar_missao(self, missao_id, quantidade):
        if missao_id in self.missoes and not self.missoes[missao_id]['completa']:
            self.missoes[missao_id]['quantidade'] += quantidade

            if self.missoes[missao_id]['quantidade'] >= self.missoes[missao_id]['alvo']:
                self.missoes[missao_id]['completa'] = True
                recompensa = self.missoes[missao_id]['recompensa']
                self.player.ouro += recompensa
                self.log_mensagem(f"Missão completa! Recebeu {recompensa} de ouro!")

    def get_active_missions(self):
        return [m for m in self.missoes.values() if not m['completa']]

