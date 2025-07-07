from collections import defaultdict
import random

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.nivel = 1
        self.vida = 100
        self.vida_max = 100
        self.ataque = 10
        self.defesa = 5
        self.xp = 0
        self.ouro = 0
        self.habilidades = ['Ataque Básico']
        self.classe = None
        self.inventario = defaultdict(int)

    def verificar_subir_nivel(self, log_callback):
        if self.xp >= self.nivel * 100:
            self.nivel += 1
            self.xp = 0
            self.vida_max += 20
            self.vida = self.vida_max
            self.ataque += 3
            self.defesa += 2

            # Classes ganham bônus adicionais
            if self.classe == 'Guerreiro':
                self.ataque += 2
                self.vida_max += 10
                self.vida += 10
            elif self.classe == 'Mago':
                self.ataque += 4
            elif self.classe == 'Arqueiro':
                self.ataque += 3
                self.defesa += 1

            log_callback(f"Parabéns! Você subiu para o nível {self.nivel}!")

    def escolher_classe(self, log_callback, getch_callback, os_system_callback):
        while True:
            os_system_callback('cls' if os_system_callback.__name__ == 'system' else 'clear')
            print("=== ESCOLHA SUA CLASSE ===")
            print("1. Guerreiro (+10 Vida, +5 Ataque, Golpe Poderoso)")
            print("2. Mago (+5 Ataque, Bola de Fogo)")
            print("3. Arqueiro (+3 Ataque, +1 Defesa, Chuva de Flechas)")

            opcao = getch_callback().decode('utf-8')

            if opcao == '1':
                self.classe = 'Guerreiro'
                self.vida_max += 10
                self.vida += 10
                self.ataque += 5
                self.habilidades.append('Golpe Poderoso')
                log_callback("Você agora é um Guerreiro!")
                break
            elif opcao == '2':
                self.classe = 'Mago'
                self.ataque += 5
                self.habilidades.append('Bola de Fogo')
                log_callback("Você agora é um Mago!")
                break
            elif opcao == '3':
                self.classe = 'Arqueiro'
                self.ataque += 3
                self.defesa += 1
                self.habilidades.append('Chuva de Flechas')
                log_callback("Você agora é um Arqueiro!")
                break

    def usar_item(self, item_nome, log_callback):
        if item_nome == 'Poção de Vida':
            if self.inventario[item_nome] > 0:
                cura = 30
                self.vida = min(self.vida + cura, self.vida_max)
                self.inventario[item_nome] -= 1
                log_callback(f"Usou {item_nome}! Recuperou {cura} de vida!")
            else:
                log_callback(f"Você não tem {item_nome}!")
        elif item_nome == 'Poção de Ataque':
            if self.inventario[item_nome] > 0:
                self.ataque += 5 # Este efeito é temporário no original, mas aqui é permanente
                self.inventario[item_nome] -= 1
                log_callback(f"Usou {item_nome}! Ataque aumentado em 5!")
            else:
                log_callback(f"Você não tem {item_nome}!")
        else:
            log_callback("Item não pode ser usado desta forma!")

    def coletar_item(self, item_data, log_callback, mission_system_callback):
        if item_data['tipo'] == 'Ouro':
            self.ouro += item_data['quantidade']
            log_callback(f"Coletou {item_data['quantidade']} de ouro!")
            mission_system_callback('coletar_ouro', item_data['quantidade'])
        elif item_data['tipo'] == 'Pergaminho':
            nova_habilidade = random.choice(['Golpe Crítico', 'Cura Rápida', 'Ataque Duplo'])
            self.habilidades.append(nova_habilidade)
            log_callback(f"Você aprendeu uma nova habilidade: {nova_habilidade}!")
        else:
            self.inventario[item_data['tipo']] += item_data['quantidade']
            log_callback(f"Coletou {item_data['tipo']}!")

