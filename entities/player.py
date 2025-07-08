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
        self.classe = None
        self.inventario = defaultdict(int)

        # Habilidades agora são um dicionário vazio
        self.habilidades = {}
        self.ataques_realizados = 0

    def verificar_subir_nivel(self, log_callback):
        if self.xp >= self.nivel * 100:
            self.nivel += 1
            self.xp = 0
            self.vida_max += 20
            self.vida = self.vida_max
            self.ataque += 3
            self.defesa += 2

            log_callback(f"Parabéns! Você subiu para o nível {self.nivel}!")

            # Desbloquear habilidades ao subir de nível
            self.desbloquear_habilidades()

    def desbloquear_habilidades(self):
        if self.nivel == 2 and self.classe == 'Mago':
            self.habilidades['Bola de Fogo'] = {'cooldown': 0, 'cooldown_max': 12, 'usos': 0}
        elif self.nivel == 2 and self.classe == 'Guerreiro':
            self.habilidades['Golpe Poderoso'] = {'cooldown': 0, 'cooldown_max': 3, 'usos': 0}
        elif self.nivel == 3 and self.classe == 'Arqueiro':
            self.habilidades['Chuva de Flechas'] = {'cooldown': 0, 'cooldown_max': 8, 'usos': 0}
        # Adicione mais condições conforme necessário para desbloquear habilidades em níveis diferentes

    def escolher_classe(self, log_callback, getch_callback, os_system_callback):
        while True:
            os_system_callback('cls' if os_system_callback.__name__ == 'system' else 'clear')
            print("=== ESCOLHA SUA CLASSE ===")
            print("1. Guerreiro (+10 Vida, +5 Ataque)")
            print("2. Mago (+5 Ataque, -1 defesa)")
            print("3. Arqueiro (+3 Ataque, +1 Defesa)")

            opcao = getch_callback().decode('utf-8')

            if opcao == '1':
                self.classe = 'Guerreiro'
                self.vida_max += 10
                self.vida += 10
                self.ataque += 5
                # Adiciona a habilidade ao escolher a classe
                self.habilidades['Golpe Poderoso'] = {'cooldown': 0, 'cooldown_max': 3, 'usos': 0}
                log_callback("Você agora é um Guerreiro!")
                break
            elif opcao == '2':
                self.classe = 'Mago'
                self.ataque += 5
                self.defesa += 1
                # Adiciona a habilidade ao escolher a classe
                self.habilidades['Bola de Fogo'] = {'cooldown': 0, 'cooldown_max': 22, 'usos': 0}
                log_callback("Você agora é um Mago!")
                break
            elif opcao == '3':
                self.classe = 'Arqueiro'
                self.ataque += 3
                self.defesa += 1
                # Adiciona a habilidade ao escolher a classe
                self.habilidades['Chuva de Flechas'] = {'cooldown': 0, 'cooldown_max': 8, 'usos': 0}
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
        if item_data.tipo == 'Ouro':
            self.ouro += item_data.quantidade  
            log_callback(f"Coletou {item_data.quantidade} de ouro!")
            mission_system_callback('coletar_ouro', item_data.quantidade)
        elif item_data.tipo == 'Pergaminho':  
            # Definir as propriedades de cooldown para as habilidades que podem ser aprendidas por pergaminho
            habilidades_pergaminho = {
                'Golpe Crítico': {'cooldown': 0, 'cooldown_max': 4, 'usos': 0},
                'Cura Rápida': {'cooldown': 0, 'cooldown_max': 5, 'usos': 0},
                'Ataque Duplo': {'cooldown': 0, 'cooldown_max': 6, 'usos': 0}
            }
            nova_habilidade_nome = random.choice(list(habilidades_pergaminho.keys()))
            
            # Adiciona a habilidade ao dicionário, se já não a tiver
            if nova_habilidade_nome not in self.habilidades:
                self.habilidades[nova_habilidade_nome] = habilidades_pergaminho[nova_habilidade_nome]
                log_callback(f"Você aprendeu uma nova habilidade: {nova_habilidade_nome}!")
            else:
                log_callback(f"Você encontrou um pergaminho, mas já conhece {nova_habilidade_nome}!")
        else:
            self.inventario[item_data.tipo] += item_data.quantidade  
            log_callback(f"Coletou {item_data.tipo}!")

    def reduzir_cooldown(self):
        for habilidade_nome, dados_habilidade in self.habilidades.items():
            if dados_habilidade['cooldown'] > 0:
                dados_habilidade['cooldown'] -= 1

    def pode_usar_habilidade(self, nome_habilidade):
        return nome_habilidade in self.habilidades and self.habilidades[nome_habilidade]['cooldown'] <= 0

    def usar_habilidade(self, nome_habilidade):
        if self.pode_usar_habilidade(nome_habilidade):
            self.habilidades[nome_habilidade]['cooldown'] = self.habilidades[nome_habilidade]['cooldown_max']
            self.habilidades[nome_habilidade]['usos'] += 1
            return True
        return False
