# entities/player.py
from collections import defaultdict
import random
from data.habilidades import HABILIDADES_DATA # Importa o dicionário de habilidades

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

        self.habilidades = {}
        self.ataques_realizados = 0

        self.precisao = 80
        self.esquiva = 10

        self.efeitos_ativos = {}

        # Não precisamos mais de self.todas_habilidades_base aqui,
        # pois importamos de data/habilidades.py

    def verificar_subir_nivel(self, log_callback):
        if self.xp >= self.nivel * 100:
            self.nivel += 1
            self.xp = 0
            self.vida_max += 20
            self.vida = self.vida_max
            self.ataque += 3
            self.defesa += 2
            self.precisao += 1
            self.esquiva += 0.5

            log_callback(f"Parabéns! Você subiu para o nível {self.nivel}!")
            self.desbloquear_habilidades(log_callback)

    def _aprender_habilidade(self, nome_habilidade, log_callback):
        # Agora usa HABILIDADES_DATA importado
        if nome_habilidade not in self.habilidades and nome_habilidade in HABILIDADES_DATA:
            habilidade_data_base = HABILIDADES_DATA[nome_habilidade]
            # Cria uma cópia para não modificar o dicionário original
            habilidade_instancia = {
                'cooldown': 0,
                'cooldown_max': habilidade_data_base['cooldown_max'],
                'usos': 0,
                'tipo': habilidade_data_base['tipo'],
                'descricao': habilidade_data_base.get('descricao', 'Sem descrição.'),
                'efeito_combate': habilidade_data_base['efeito_combate'] # Mantém a referência para o CombatSystem
            }
            self.habilidades[nome_habilidade] = habilidade_instancia
            log_callback(f"Você aprendeu {nome_habilidade}!")

    def desbloquear_habilidades(self, log_callback):
        # Habilidades de Guerreiro
        if self.classe == 'Guerreiro':
            if self.nivel == 2:
                self._aprender_habilidade('Ataque Giratório', log_callback)
            if self.nivel == 4:
                self._aprender_habilidade('Investida Brutal', log_callback)
            if self.nivel == 6: # Nova habilidade para Guerreiro
                self._aprender_habilidade('Grito de Guerra', log_callback)
        # Habilidades de Mago
        elif self.classe == 'Mago':
            if self.nivel == 2:
                self._aprender_habilidade('Cura Menor', log_callback)
            if self.nivel == 4:
                self._aprender_habilidade('Raio Arcano', log_callback)
            if self.nivel == 6: # Nova habilidade para Mago
                self._aprender_habilidade('Escudo de Mana', log_callback)
        # Habilidades de Arqueiro
        elif self.classe == 'Arqueiro':
            if self.nivel == 3:
                self._aprender_habilidade('Tiro Preciso', log_callback)
            if self.nivel == 5:
                self._aprender_habilidade('Tiro Múltiplo', log_callback)
        # Habilidades de Ladrão
        elif self.classe == 'Ladrão':
            if self.nivel == 2:
                self._aprender_habilidade('Ataque Furtivo', log_callback)
            if self.nivel == 4:
                self._aprender_habilidade('Distração', log_callback)
            if self.nivel == 6: # Nova habilidade para Ladrão
                self._aprender_habilidade('Ataque Venenoso', log_callback)
        # Habilidades de Clérigo
        elif self.classe == 'Clérigo':
            if self.nivel == 2:
                self._aprender_habilidade('Escudo Divino', log_callback)
            if self.nivel == 4:
                self._aprender_habilidade('Bênção Divina', log_callback)
        # Adicione mais condições conforme necessário para desbloquear habilidades em níveis diferentes

    def escolher_classe(self, log_callback, getch_callback, os_system_callback):
        while True:
            os_system_callback('cls' if os_system_callback.__name__ == 'system' else 'clear')
            print("=== ESCOLHA SUA CLASSE ===")
            print("1. Guerreiro (+10 Vida, +5 Ataque, +5 Precisão)")
            print("2. Mago (+5 Ataque, +1 Defesa, +5 Precisão)")
            print("3. Arqueiro (+3 Ataque, +1 Defesa, +10 Precisão, +5 Esquiva)")
            print("4. Ladrão (+5 Ataque, +10 Esquiva, +5 Precisão)")
            print("5. Clérigo (+20 Vida, +2 Defesa, +5 Precisão)")

            opcao = getch_callback().decode('utf-8')

            if opcao == '1':
                self.classe = 'Guerreiro'
                self.vida_max += 10
                self.vida += 10
                self.ataque += 5
                self.precisao += 5
                self._aprender_habilidade('Golpe Poderoso', log_callback)
                log_callback("Você agora é um Guerreiro!")
                break
            elif opcao == '2':
                self.classe = 'Mago'
                self.ataque += 5
                self.defesa += 1
                self.precisao += 5
                self._aprender_habilidade('Bola de Fogo', log_callback)
                log_callback("Você agora é um Mago!")
                break
            elif opcao == '3':
                self.classe = 'Arqueiro'
                self.ataque += 3
                self.defesa += 1
                self.precisao += 10
                self.esquiva += 5
                self._aprender_habilidade('Chuva de Flechas', log_callback)
                log_callback("Você agora é um Arqueiro!")
                break
            elif opcao == '4':
                self.classe = 'Ladrão'
                self.ataque += 5
                self.esquiva += 10
                self.precisao += 5
                self._aprender_habilidade('Ataque Rápido', log_callback)
                log_callback("Você agora é um Ladrão!")
                break
            elif opcao == '5':
                self.classe = 'Clérigo'
                self.vida_max += 20
                self.vida += 20
                self.defesa += 2
                self.precisao += 5
                self._aprender_habilidade('Cura Leve', log_callback)
                log_callback("Você agora é um Clérigo!")
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
                if 'Poção de Ataque' not in self.efeitos_ativos:
                    self.ataque += 5
                    self.efeitos_ativos['Poção de Ataque'] = {'turnos_restantes': 3, 'valor': 5, 'tipo': 'buff_ataque'}
                    log_callback(f"Usou {item_nome}! Ataque aumentado em 5 por 3 turnos!")
                else:
                    log_callback(f"O efeito de {item_nome} já está ativo!")
                self.inventario[item_nome] -= 1
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
            # Pega todas as habilidades que não são de classe inicial
            habilidades_pergaminho_nomes = [
                nome for nome, data in HABILIDADES_DATA.items()
                if nome not in ['Ataque Básico', 'Golpe Poderoso', 'Bola de Fogo', 'Chuva de Flechas',
                                'Ataque Rápido', 'Cura Leve'] # Habilidades iniciais de classe
            ]
            nova_habilidade_nome = random.choice(habilidades_pergaminho_nomes)

            if nova_habilidade_nome not in self.habilidades:
                self._aprender_habilidade(nova_habilidade_nome, log_callback)
            else:
                log_callback(f"Você encontrou um pergaminho, mas já conhece {nova_habilidade_nome}!")
        else:
            self.inventario[item_data.tipo] += item_data.quantidade
            log_callback(f"Coletou {item_data.tipo}!")

    def reduzir_cooldown(self, log_callback):
        for habilidade_nome, dados_habilidade in self.habilidades.items():
            if dados_habilidade['cooldown'] > 0:
                dados_habilidade['cooldown'] -= 1

        efeitos_para_remover = []
        for efeito_nome, dados_efeito in self.efeitos_ativos.items():
            dados_efeito['turnos_restantes'] -= 1
            if dados_efeito['turnos_restantes'] <= 0:
                efeitos_para_remover.append(efeito_nome)
                if dados_efeito['tipo'] == 'buff_ataque':
                    self.ataque -= dados_efeito['valor']
                    log_callback(f"O efeito de {efeito_nome} terminou. Seu ataque voltou ao normal.")
                elif dados_efeito['tipo'] == 'buff_defesa':
                    self.defesa -= dados_efeito['valor']
                    log_callback(f"O efeito de {efeito_nome} terminou. Sua defesa voltou ao normal.")
                elif dados_efeito['tipo'] == 'buff_precisao':
                    self.precisao -= dados_efeito['valor']
                    log_callback(f"O efeito de {efeito_nome} terminou. Sua precisão voltou ao normal.")
                # Adicione aqui a reversão de outros buffs/debuffs do jogador
                # Ex: if dados_efeito['tipo'] == 'escudo_de_mana': self.vida_max_temporaria -= dados_efeito['valor']
        for efeito_nome in efeitos_para_remover:
            del self.efeitos_ativos[efeito_nome]

        # Lógica para efeitos ativos no inimigo (se implementado)
        # Isso exigiria que o inimigo tivesse um dicionário de efeitos_ativos
        # e que o CombatSystem chamasse um método para reduzir cooldowns do inimigo.
        # Por enquanto, vamos assumir que o inimigo não tem efeitos_ativos persistentes.

    def pode_usar_habilidade(self, nome_habilidade):
        return nome_habilidade in self.habilidades and self.habilidades[nome_habilidade]['cooldown'] <= 0

    def usar_habilidade(self, nome_habilidade):
        if self.pode_usar_habilidade(nome_habilidade):
            self.habilidades[nome_habilidade]['cooldown'] = self.habilidades[nome_habilidade]['cooldown_max']
            self.habilidades[nome_habilidade]['usos'] += 1
            return True
        return False

