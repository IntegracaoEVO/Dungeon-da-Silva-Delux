import random

class CombatSystem:
    def __init__(self, player, log_callback, game_over_callback, mission_system_callback):
        self.player = player
        self.log_mensagem = log_callback
        self.game_over = game_over_callback
        self.mission_system_callback = mission_system_callback
        self.current_enemy = None

    def iniciar_combate(self, enemy):
        self.current_enemy = enemy
        self.log_mensagem(f"Combate iniciado com {enemy.tipo}!")
        # Atualiza missão de matar goblins
        if enemy.tipo == 'Goblin':
            self.mission_system_callback('matar_goblins', 1)
        return "combate" # Retorna o novo estado do jogo

    def resolver_combate_acao(self, acao):
        if not self.current_enemy:
            return "explorando" # Deve estar em combate para resolver ações

        inimigo = self.current_enemy
        jogador = self.player

        if acao == 'atacar':
            dano = max(1, jogador.ataque - inimigo.defesa // 2)
            inimigo.vida -= dano
            self.log_mensagem(f"Você atacou e causou {dano} de dano!")

            if inimigo.vida <= 0:
                return self._derrotar_inimigo(inimigo)

            dano_inimigo = max(1, inimigo.ataque - jogador.defesa // 2)
            jogador.vida -= dano_inimigo
            self.log_mensagem(f"{inimigo.tipo} contra-atacou causando {dano_inimigo} de dano!")

            if jogador.vida <= 0:
                self.game_over()
                return "game_over" # Estado de game over
            return "combate"

        elif acao == 'fugir':
            if random.random() < 0.5:
                self.log_mensagem("Você fugiu do combate!")
                self.current_enemy = None
                return "explorando"
            else:
                self.log_mensagem("Falha ao fugir! O inimigo ataca!")
                dano_inimigo = max(1, inimigo.ataque - jogador.defesa // 2)
                jogador.vida -= dano_inimigo
                self.log_mensagem(f"{inimigo.tipo} atacou causando {dano_inimigo} de dano!")

                if jogador.vida <= 0:
                    self.game_over()
                    return "game_over"
                return "combate"
        return "combate" # Permanece em combate se a ação não for fuga ou derrota

    def _derrotar_inimigo(self, inimigo):
        self.player.xp += inimigo.xp
        self.player.ouro += inimigo.ouro

    # Adicione esta linha para remover o inimigo do mapa
        if hasattr(self, 'game_map'):  # Verifica se temos acesso ao game_map
            self.game_map.remove_entity(inimigo)

        if inimigo.chefao:
            self.log_mensagem(f"VITÓRIA! Você derrotou o {inimigo.tipo}!")
            self.current_enemy = None
            self.player.verificar_subir_nivel(self.log_mensagem)
            return "vitoria"
        else:
            self.log_mensagem(f"Você derrotou o {inimigo.tipo} e ganhou {inimigo.xp} XP e {inimigo.ouro} de ouro!")
            self.current_enemy = None
            self.player.verificar_subir_nivel(self.log_mensagem)
        return "explorando"

    def aplicar_habilidade(self, habilidade):
        inimigo = self.current_enemy
        jogador = self.player

        if habilidade == 'Ataque Básico':
            return self.resolver_combate_acao('atacar')
        elif habilidade == 'Golpe Poderoso':
            dano = max(1, jogador.ataque * 2 - inimigo.defesa // 2)
            inimigo.vida -= dano
            self.log_mensagem(f"Golpe Poderoso! Causou {dano} de dano!")

            if inimigo.vida <= 0:
                return self._derrotar_inimigo(inimigo)
            else:
                dano_inimigo = max(1, inimigo.ataque - jogador.defesa // 2)
                jogador.vida -= dano_inimigo
                self.log_mensagem(f"{inimigo.tipo} contra-atacou causando {dano_inimigo} de dano!")
                if jogador.vida <= 0:
                    self.game_over()
                    return "game_over"
                return "combate"
        elif habilidade == 'Bola de Fogo':
            dano = max(1, jogador.ataque * 3 - inimigo.defesa // 4)
            inimigo.vida -= dano
            self.log_mensagem(f"Bola de Fogo! Causou {dano} de dano!")

            if inimigo.vida <= 0:
                return self._derrotar_inimigo(inimigo)
            else:
                dano_inimigo = max(1, inimigo.ataque - jogador.defesa // 2)
                jogador.vida -= dano_inimigo
                self.log_mensagem(f"{inimigo.tipo} contra-atacou causando {dano_inimigo} de dano!")
                if jogador.vida <= 0:
                    self.game_over()
                    return "game_over"
                return "combate"
        elif habilidade == 'Cura Rápida':
            cura = 25
            jogador.vida = min(jogador.vida + cura, jogador.vida_max)
            self.log_mensagem(f"Cura Rápida! Recuperou {cura} de vida!")

            dano_inimigo = max(1, inimigo.ataque - jogador.defesa // 2)
            jogador.vida -= dano_inimigo
            self.log_mensagem(f"{inimigo.tipo} atacou causando {dano_inimigo} de dano!")

            if jogador.vida <= 0:
                self.game_over()
                return "game_over"
            return "combate"
        else:
            self.log_mensagem("Habilidade não implementada!")
            return "combate"

    def usar_item_combate(self, item_nome):
        if self.player.inventario.get(item_nome, 0) > 0:
            self.player.usar_item(item_nome, self.log_mensagem)
            # Inimigo ataca após o uso do item
            inimigo = self.current_enemy
            jogador = self.player
            dano_inimigo = max(1, inimigo.ataque - jogador.defesa // 2)
            jogador.vida -= dano_inimigo
            self.log_mensagem(f"{inimigo.tipo} atacou causando {dano_inimigo} de dano!")
            if jogador.vida <= 0:
                self.game_over()
                return "game_over"
            return "combate"
        else:
            self.log_mensagem("Você não tem este item!")
            return "combate"

