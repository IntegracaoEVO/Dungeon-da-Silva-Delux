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

    def _mostrar_loja(self):
        print("=== LOJA DO MERCADOR ===")
        print(f"Seu ouro: {self.player.ouro}")
    
        itens = {
            "1": {"nome": "Poção de Vida", "preco": 10, "tipo": "consumivel"},
            "2": {"nome": "Poção de Ataque", "preco": 15, "tipo": "consumivel"},
            "3": {"nome": "Pergaminho Mágico", "preco": 25, "tipo": "habilidade"}
        }
        
        for cod, item in itens.items():
            print(f"{cod}. {item['nome']} - {item['preco']} ouro")
        
            print("0. Sair")
        
        while True:
            opcao = input("Escolha uma opção: ")
            if opcao == '0':
                print("Saindo da loja...")
                break
            elif opcao in itens:
                self._comprar_item(itens[opcao])
                break
            else:
                print("Opção inválida! Tente novamente.")


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
        for idx, (nome_hab, dados_hab) in enumerate(self.player.habilidades.items(), 1):
            cooldown_info = f" (CD: {dados_hab['cooldown']})" if dados_hab['cooldown'] > 0 else ""
            print(f"{idx}. {nome_hab}{cooldown_info}")

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


    def _mostrar_combate(self):
        inimigo = self.combat_system.current_enemy
        if not inimigo:
            return

        # Sprite do jogador (simplificado)
        player_sprite = [
            "  O  ",
            " /|\\ ",
            " / \\ "
        ]
        
        # Sprite do inimigo (varia por tipo)
        enemy_sprite = {
            'Goblin': [
                "  G  ",
                " /|\\ ",
                " | | "
            ],
            'Orc': [
                " _O_ ",
                "| o |",
                "|___|"
            ],
            'Dragão': [
                " .^. ",
                "/O O\\",
                " > < "
            ],
            'Morto-Vivo': [
                " x_x ",
                " |\\| ",
                " / \\ "
            ],
            'Slime':[
                "     ",
                " ~~~ ",
                "(o_o)"
            ]
        }

        # Obter o sprite do inimigo com base no tipo
        enemy_sprite_lines = enemy_sprite.get(inimigo.tipo, [
            " ? ",
            "/|\\",
            " | "
        ])

        # Barra de vida do jogador
        vida_jogador = f"Jogador: [{'#' * int(10 * self.player.vida/self.player.vida_max)}{' ' * (10 - int(10 * self.player.vida/self.player.vida_max))}] {self.player.vida}/{self.player.vida_max}"
        
        # Barra de vida do inimigo
        vida_inimigo = f"Inimigo: [{'#' * int(10 * inimigo.vida/inimigo.vida_max)}{' ' * (10 - int(10 * inimigo.vida/inimigo.vida_max))}] {inimigo.vida}/{inimigo.vida_max}"

        # Exibir interface
        print("\n=== COMBATE ===")
        print("Jogador".center(20) + "VS".center(10) + inimigo.tipo.center(20))
        
        # Exibir sprites lado a lado
        for p_line, e_line in zip(player_sprite, enemy_sprite_lines):
            print(p_line.center(20) + "".center(10) + e_line.center(20))
        
        print("\n" + vida_jogador)
        print(vida_inimigo + "\n")
        
        print("\nAções:")
        print("1. Atacar")
        print("2. Usar Habilidade")
        print("3. Usar Item")
        print("4. Fugir (50% chance)")


    def _mostrar_vitoria(self):
        print("=== VITÓRIA EPICA ===")
        print(f"Parabéns! Você derrotou o chefão da dungeon nível {self.game_map.dungeon_nivel}!")
        print("\nRecompensas:")
        # Acessa XP e Ouro do inimigo derrotado
        if self.combat_system.current_enemy:
            print(f"- {self.combat_system.current_enemy.xp} XP")
            print(f"- {self.combat_system.current_enemy.ouro} de ouro")
        else:
            print("- Recompensas já coletadas ou inimigo não definido.")
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
            # Reduzir cooldowns ao iniciar combate (opcional, dependendo da sua lógica de turno)
            self.player.reduzir_cooldown() 
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
            # Reduzir cooldowns ao mudar de nível (opcional)
            self.player.reduzir_cooldown()
            return

        self.player.x, self.player.y = novo_x, novo_y
        # Reduzir cooldowns a cada movimento (se quiser um cooldown baseado em "passos")
        # self.player.reduzir_cooldown()


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
                # Reduzir cooldowns após cada ação de exploração (se não for por movimento)
                # self.player.reduzir_cooldown()

            elif current_state == "combate":
                # Reduzir cooldowns no início do turno do jogador em combate
                self.player.reduzir_cooldown() 

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
        # Pega apenas os nomes das habilidades para exibir no menu de seleção
        habilidades_nomes = list(self.player.habilidades.keys())

        if not habilidades_nomes:
            self.game_state.log_mensagem("Você não tem habilidades!")
            return

        while True:
            self.game_state.clear_screen()
            print("=== HABILIDADES ===")
            # Exibe o nome da habilidade e o cooldown
            for idx, nome_hab in enumerate(habilidades_nomes, 1):
                dados_hab = self.player.habilidades[nome_hab]
                cooldown_info = f" (CD: {dados_hab['cooldown']})" if dados_hab['cooldown'] > 0 else ""
                print(f"{idx}. {nome_hab}{cooldown_info}")
            print("0. Voltar")

            opcao = msvcrt.getch().decode('utf-8')

            if opcao == '0':
                break
            elif opcao.isdigit() and 1 <= int(opcao) <= len(habilidades_nomes):
                habilidade_selecionada_nome = habilidades_nomes[int(opcao)-1]
                
                # Verifica se a habilidade pode ser usada (cooldown)
                if self.player.pode_usar_habilidade(habilidade_selecionada_nome):
                    new_state = self.combat_system.aplicar_habilidade(habilidade_selecionada_nome)
                    # Se a habilidade foi usada com sucesso, aplica o cooldown
                    if new_state == "combate" or new_state == "explorando" or new_state == "vitoria": # Habilidade resultou em um estado válido
                        self.player.usar_habilidade(habilidade_selecionada_nome) # Aplica o cooldown
                    self.game_state.set_state(new_state)
                    break
                else:
                    self.game_state.log_mensagem(f"{habilidade_selecionada_nome} está em cooldown! ({self.player.habilidades[habilidade_selecionada_nome]['cooldown']} turnos restantes)")
                    # Não quebra o loop, permite que o jogador escolha outra habilidade ou volte
            else:
                self.game_state.log_mensagem("Opção inválida!")


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

