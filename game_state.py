import os

class GameState:
    def __init__(self):
        self.current_state = "explorando"  # explorando | combate | menu | loja | vitoria | game_over
        self.historico = []
        self.inimigo_combate = None # Referência ao inimigo atual em combate

    def set_state(self, new_state):
        self.current_state = new_state

    def get_state(self):
        return self.current_state

    def log_mensagem(self, msg):
        self.historico.append(msg)
        if len(self.historico) > 5:
            self.historico.pop(0)

    def get_historico(self):
        return self.historico

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

