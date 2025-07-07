import os
import msvcrt # Para Windows. Para Linux/Mac, usar sys, tty, termios
import sys

# Importar classes modularizadas
from entities.player import Player
from entities.enemy import Enemy
from entities.item import Item
from entities.npc import NPC
from systems.combat_system import CombatSystem
from systems.mission_system import MissionSystem
from systems.shop_system import ShopSystem
from game_map import GameMap
from game_state import GameState

# Para Linux/Mac, substitua msvcrt por:
# def getch():
#     fd = sys.stdin.fileno()
#     old_settings = termios.tcgetattr(fd)
#     try:
#         tty.setraw(sys.stdin.fileno())
#         ch = sys.stdin.read(1)
#     finally:
#         termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#     return ch.encode('utf-8') # Retorna bytes para compatibilidade

class JogoRPG:
    def __init__(self):
        self.player = Player()
        self.game_state = GameState()
        self.game_map = GameMap(largura=50, altura=30)

    # Inicializar sistemas, passando referências necessárias
        self.mission_system = MissionSystem(self.player, self.game_state.log_mensagem)
        self.combat_system = CombatSystem(self.player, self.game_state.log_mensagem, self.game_over, self.mission_system.atualizar_missao)
        self.shop_system = ShopSystem(self.player, self.game_state.log_mensagem)
    
    # Adicione esta linha para passar a referência do game_map para o combat_system
        self.combat_system.game_map = self.game_map

        self.game_map.gerar_dungeon(self.player)

    def mostrar_tela(self):
        self.game_state.clear_screen()

        if self.game_state.get_state() == "explorando":
            self._mostrar_mapa()
        elif self.game_state.get_state() == "combate":
            self._mostrar_combate()
        elif self.game_state.get_state() == "menu":
            self._mostrar_menu()
        elif self.game_state.get_state() == "loja":
            self._mostrar_loja()
        elif self.game_state.get_state() == "vitoria":
            self._mostrar_vitoria()

        self._mostrar_historico()

    def _mostrar_mapa(self):
        print(f"=== Dungeon Nível {self.game_map.dungeon_nivel} ===")
        print(f"Vida: {self.player.vida}/{self.player.vida_max} | Nível: {self.player.nivel} | XP: {self.player.xp}/{self.player.nivel*100}")
        print(f"Ouro: {self.player.ouro} | Ataque: {self.player.ataque} | Defesa: {self.player.defesa}")
        print("WASD: Mover | E: Menu | Q: Sair | L: Loja (perto de mercador)")

        raio_visao = 10
        x_min = max(0, self.player.x - raio_visao)
        x_max = min(self.game_map.largura, self.player.x + raio_visao + 1)
        y_min = max(0, self.player.y - raio_visao//2)
        y_max = min(self.game_map.altura, self.player.y + raio_visao//2 + 1)

        for y in range(y_min, y_max):
            linha = ''
            for x in range(x_min, x_max):
                if x == self.player.x and y == self.player.y:
                    linha += '@'
                else:
                    celula = self.game_map.mapa[y][x]
                    inimigo, item, portal, npc = self.game_map.get_entities_at_position(x, y)

                    if inimigo:
                        linha += 'E' if not inimigo.chefao else 'D'
                    elif item:
                        linha += 'i'
                    elif portal:
                        linha += 'O'
                    elif npc:
                        linha += 'M'
                    else:
                        linha += celula
            print(linha)

        print("\nMissões:")
        for missao in self.mission_system.get_active_missions():
            print(f"- {missao['objetivo']} ({missao['quantidade']}/{missao['alvo']})")

    def _mostrar_combate(self):
        inimigo = self.combat_system.current_enemy
        if not inimigo:
            self.game_state.log_mensagem("Erro: Nenhum inimigo em combate.")
            self.game_state.set_state("explorando")
            return

        print(f"=== COMBATE vs {inimigo.tipo} ===")
        print(f"Sua Vida: {self.player.vida}/{self.player.vida_max}")
        print(f"Inimigo Vida: {inimigo.vida}/{inimigo.vida_max}")

        print("\nAções:")
        print("1. Atacar")
        print("2. Usar Habilidade")
        print("3. Usar Item")
        print("4. Fugir (50% chance)")

        if inimigo.chefao:
            print("\nDICA: Este é um chefão! Use itens e habilidades com cuidado!")

    def _mostrar_menu(self):
        print("=== MENU ===")
        print(f"Classe: {self.player.classe or 'Nenhuma'}")
        print(f"Nível: {self.player.nivel}")
        print(f"Vida: {self.player.vida}/{self.player.vida_max}")
        print(f"Ataque: {self.player.ataque}")
        print(f"Defesa: {self.player.defesa}")
        print(f"XP: {self.player.xp}/{self.player.nivel*100}")
        print(f"Ouro: {self.player.ouro}")

        print("\nHabilidades:")
        for idx, hab in enumerate(self.player.habilidades, 1):
            print(f"{idx}. {hab}")

        print("\nInventário:")
        if not self.player.inventario:
            print("- Vazio")
        else:
            for item, qtd in self.player.inventario.items():
                print(f"- {item}: {qtd}")

        print("\n1. Usar Poção de Vida")
        print("2. Usar Poção de Ataque")
        if not self.player.classe:
            print("3. Escolher Classe (uma vez)")
        print("0. Voltar")

    def _mostrar_loja(self):
        print("=== LOJA DO MERCADOR ===")
        print(f"Ouro: {self.player.ouro}")

        for idx, item in enumerate(self.shop_system.get_shop_items(), 1):
            print(f"{idx}. {item.nome} - {item.preco} ouro")

        print("\n0. Voltar")

    def _mostrar_vitoria(self):
        print("=== VITÓRIA EPICA ===")
        print(f"Parabéns! Você derrotou o chefão da dungeon nível {self.game_map.dungeon_nivel}!")
        print("\nRecompensas:")
        print(f"- {self.combat_system.current_enemy.xp} XP")
        print(f"- {self.combat_system.current_enemy.ouro} de ouro")
        print("\nPressione qualquer tecla para continuar explorando...")

    def _mostrar_historico(self):
        if self.game_state.get_historico():
            print("\nÚltimas mensagens:")
            for msg in self.game_state.get_historico()[-3:]:
                print(f"- {msg}")

    def mover_jogador(self, direcao):
        if self.game_state.get_state() != "explorando":
            return

        dx, dy = 0, 0
        if direcao == 'cima':
            dy = -1
        elif direcao == 'baixo':
            dy = 1
        elif direcao == 'esquerda':
            dx = -1
        elif direcao == 'direita':
            dx = 1

        novo_x = self.player.x + dx
        novo_y = self.player.y + dy

        if not (0 <= novo_x < self.game_map.largura and 0 <= novo_y < self.game_map.altura):
            self.game_state.log_mensagem("Você atingiu os limites da dungeon!")
            return

        if self.game_map.mapa[novo_y][novo_x] == '#':
            self.game_state.log_mensagem("Há uma parede no caminho!")
            return

        inimigo, item, portal, npc = self.game_map.get_entities_at_position(novo_x, novo_y)

        if inimigo:
            self.game_state.set_state(self.combat_system.iniciar_combate(inimigo))
            return
        elif item:
            self.player.coletar_item(item, self.game_state.log_mensagem, self.mission_system.atualizar_missao)
            self.game_map.remove_entity(item)
        elif npc:
            self.game_state.log_mensagem(npc.dialogo)
        elif portal:
            self.game_map.dungeon_nivel += 1
            self.game_state.log_mensagem(f"Descendo para a dungeon nível {self.game_map.dungeon_nivel}...")
            self.game_map.gerar_dungeon(self.player)
            return

        self.player.x, self.player.y = novo_x, novo_y

    def game_over(self):
        self.game_state.clear_screen()
        print("=== GAME OVER ===")
        print(f"Você chegou ao nível {self.player.nivel} na dungeon nível {self.game_map.dungeon_nivel}.")
        print("\nDeseja jogar novamente? (s/n)")

        while True:
            opcao = msvcrt.getch().decode('utf-8').lower()
            if opcao == 's':
                self.__init__()  # Reinicia o jogo
                return
            elif opcao == 'n':
                exit()

    def run(self):
        while True:
            self.mostrar_tela()
            tecla = msvcrt.getch().decode('utf-8').lower()

            if tecla == 'q':
                print("Saindo do jogo...")
                break

            current_state = self.game_state.get_state()

            if current_state == "explorando":
                if tecla == 'e':
                    self.game_state.set_state("menu")
                elif tecla == 'l':
                    mercador = next((n for n in self.game_map.npcs if n.tipo == 'Mercador'), None)
                    if mercador and abs(self.player.x - mercador.x) <= 1 and abs(self.player.y - mercador.y) <= 1:
                        self.game_state.set_state("loja")
                    else:
                        self.game_state.log_mensagem("Nenhum mercador por perto!")
                elif tecla == 'w':
                    self.mover_jogador('cima')
                elif tecla == 's':
                    self.mover_jogador('baixo')
                elif tecla == 'a':
                    self.mover_jogador('esquerda')
                elif tecla == 'd':
                    self.mover_jogador('direita')

            elif current_state == "combate":
                if tecla == '1':
                    new_state = self.combat_system.resolver_combate_acao('atacar')
                    self.game_state.set_state(new_state)
                elif tecla == '2':
                    self._menu_habilidades_combate()
                elif tecla == '3':
                    self._menu_itens_combate()
                elif tecla == '4':
                    new_state = self.combat_system.resolver_combate_acao('fugir')
                    self.game_state.set_state(new_state)

            elif current_state == "menu":
                if tecla == '0':
                    self.game_state.set_state("explorando")
                elif tecla == '1' and self.player.inventario.get('Poção de Vida', 0) > 0:
                    self.player.usar_item('Poção de Vida', self.game_state.log_mensagem)
                    self.game_state.set_state("explorando")
                elif tecla == '2' and self.player.inventario.get('Poção de Ataque', 0) > 0:
                    self.player.usar_item('Poção de Ataque', self.game_state.log_mensagem)
                    self.game_state.set_state("explorando")
                elif tecla == '3' and not self.player.classe:
                    self.player.escolher_classe(self.game_state.log_mensagem, msvcrt.getch, os.system)
                    self.game_state.set_state("explorando")

            elif current_state == "loja":
                if tecla == '0':
                    self.game_state.set_state("explorando")
                elif tecla.isdigit() and 1 <= int(tecla) <= len(self.shop_system.get_shop_items()):
                    self.shop_system.comprar_item(int(tecla)-1)

            elif current_state == "vitoria":
                self.game_state.set_state("explorando")

    def _menu_habilidades_combate(self):
        if not self.player.habilidades:
            self.game_state.log_mensagem("Você não tem habilidades!")
            return

        while True:
            self.game_state.clear_screen()
            print("=== HABILIDADES ===")
            for idx, hab in enumerate(self.player.habilidades, 1):
                print(f"{idx}. {hab}")
            print("0. Voltar")

            opcao = msvcrt.getch().decode('utf-8')

            if opcao == '0':
                break
            elif opcao.isdigit() and 1 <= int(opcao) <= len(self.player.habilidades):
                habilidade = self.player.habilidades[int(opcao)-1]
                new_state = self.combat_system.aplicar_habilidade(habilidade)
                self.game_state.set_state(new_state)
                break

    def _menu_itens_combate(self):
        if not any(qtd > 0 for qtd in self.player.inventario.values()):
            self.game_state.log_mensagem("Você não tem itens para usar!")
            return

        while True:
            self.game_state.clear_screen()
            print("=== ITENS DE COMBATE ===")

            itens_disponiveis = [item for item, qtd in self.player.inventario.items() if qtd > 0]
            for idx, item in enumerate(itens_disponiveis, 1):
                print(f"{idx}. {item} ({self.player.inventario[item]})")
            print("0. Voltar")

            opcao = msvcrt.getch().decode('utf-8')

            if opcao == '0':
                break
            elif opcao.isdigit() and 1 <= int(opcao) <= len(itens_disponiveis):
                item_selecionado = itens_disponiveis[int(opcao)-1]
                new_state = self.combat_system.usar_item_combate(item_selecionado)
                self.game_state.set_state(new_state)
                break

if __name__ == "__main__":
    game = JogoRPG()
    game.run()

