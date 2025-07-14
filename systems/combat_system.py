# systems/combat_system.py
import random
from data.habilidades import HABILIDADES_DATA # Importa o dicionário de habilidades

class CombatSystem:
    def __init__(self, player, log_callback, game_over_callback, mission_system_callback):
        self.player = player
        self.log_mensagem = log_callback
        self.game_over = game_over_callback
        self.mission_system_callback = mission_system_callback
        self.current_enemy = None

        # Mapeamento de nomes de métodos para seus métodos de aplicação
        # Isso é mais robusto do que mapear diretamente o nome da habilidade,
        # pois permite que várias habilidades chamem o mesmo método de efeito se tiverem lógica similar.
        self.efeito_combate_map = {
            '_aplicar_ataque_basico': self._aplicar_ataque_basico,
            '_aplicar_golpe_poderoso': self._aplicar_golpe_poderoso,
            '_aplicar_bola_de_fogo': self._aplicar_bola_de_fogo,
            '_aplicar_chuva_de_flechas': self._aplicar_chuva_de_flechas,
            '_aplicar_golpe_critico': self._aplicar_golpe_critico,
            '_aplicar_ataque_duplo': self._aplicar_ataque_duplo,
            '_aplicar_ataque_rapido': self._aplicar_ataque_rapido,
            '_aplicar_ataque_furtivo': self._aplicar_ataque_furtivo,
            '_aplicar_ataque_giratorio': self._aplicar_ataque_giratorio,
            '_aplicar_cura_rapida': self._aplicar_cura_rapida,
            '_aplicar_cura_leve': self._aplicar_cura_leve,
            '_aplicar_cura_menor': self._aplicar_cura_menor,
            '_aplicar_foco_preciso': self._aplicar_foco_preciso,
            '_aplicar_pele_de_pedra': self._aplicar_pele_de_pedra,
            '_aplicar_escudo_divino': self._aplicar_escudo_divino,
            # Novas Habilidades
            '_aplicar_investida_brutal': self._aplicar_investida_brutal,
            '_aplicar_raio_arcano': self._aplicar_raio_arcano,
            '_aplicar_tiro_multiplo': self._aplicar_tiro_multiplo,
            '_aplicar_distracao': self._aplicar_distracao,
            '_aplicar_bencao_divina': self._aplicar_bencao_divina,
            '_aplicar_drenar_vida': self._aplicar_drenar_vida,
            '_aplicar_ataque_venenoso': self._aplicar_ataque_venenoso, # Nova habilidade
            '_aplicar_grito_de_guerra': self._aplicar_grito_de_guerra, # Nova habilidade
            '_aplicar_escudo_de_mana': self._aplicar_escudo_de_mana, # Nova habilidade
        }

    def iniciar_combate(self, enemy):
        self.current_enemy = enemy
        self.log_mensagem(f"Combate iniciado com {enemy.tipo}!")
        if enemy.tipo == 'Goblin':
            self.mission_system_callback('matar_goblins', 1)
        # Inicializa efeitos ativos do inimigo para debuffs
        if not hasattr(enemy, 'efeitos_ativos'):
            enemy.efeitos_ativos = {}
        return "combate"

    def _calcular_acerto(self, atacante, defensor):
        chance_acerto_base = atacante.precisao - defensor.esquiva
        chance_acerto_final = max(10, min(95, chance_acerto_base))

        if random.randint(1, 100) <= chance_acerto_final:
            return True, chance_acerto_final
        else:
            return False, chance_acerto_final

    def resolver_combate_acao(self, acao):
        if not self.current_enemy:
            return "explorando"

        inimigo = self.current_enemy
        jogador = self.player

        if acao == 'atacar':
            acertou_jogador, chance_jogador = self._calcular_acerto(jogador, inimigo)
            if acertou_jogador:
                dano = max(1, jogador.ataque - inimigo.defesa // 2)
                inimigo.vida -= dano
                self.log_mensagem(f"Você atacou e causou {dano} de dano! (Chance: {chance_jogador}%)")
            else:
                self.log_mensagem(f"Você errou o ataque! (Chance: {chance_jogador}%)")

            if inimigo.vida <= 0:
                return self._derrotar_inimigo(inimigo)

            # Aplica efeitos de status do inimigo (se houver)
            self._aplicar_efeitos_inimigo(inimigo)

            acertou_inimigo, chance_inimigo = self._calcular_acerto(inimigo, jogador)
            if acertou_inimigo:
                dano_inimigo = max(1, inimigo.ataque - jogador.defesa // 2)
                jogador.vida -= dano_inimigo
                self.log_mensagem(f"{inimigo.tipo} contra-atacou causando {dano_inimigo} de dano! (Chance: {chance_inimigo}%)")
            else:
                self.log_mensagem(f"{inimigo.tipo} errou o ataque! (Chance: {chance_inimigo}%)")

            if jogador.vida <= 0:
                self.game_over()
                return "game_over"
            return "combate"

        elif acao == 'fugir':
            if random.random() < 0.5:
                self.log_mensagem("Você fugiu do combate!")
                self.current_enemy = None
                return "explorando"
            else:
                self.log_mensagem("Falha ao fugir! O inimigo ataca!")
                # Aplica efeitos de status do inimigo (se houver)
                self._aplicar_efeitos_inimigo(inimigo)

                acertou_inimigo, chance_inimigo = self._calcular_acerto(inimigo, jogador)
                if acertou_inimigo:
                    dano_inimigo = max(1, inimigo.ataque - jogador.defesa // 2)
                    jogador.vida -= dano_inimigo
                    self.log_mensagem(f"{inimigo.tipo} atacou causando {dano_inimigo} de dano! (Chance: {chance_inimigo}%)")
                else:
                    self.log_mensagem(f"{inimigo.tipo} errou o ataque! (Chance: {chance_inimigo}%)")

                if jogador.vida <= 0:
                    self.game_over()
                    return "game_over"
                return "combate"
        return "combate"

    def _derrotar_inimigo(self, inimigo):
        self.player.xp += inimigo.xp
        self.player.ouro += inimigo.ouro

        if hasattr(self, 'game_map'):
            self.game_map.remove_entity(inimigo)

        # Limpa efeitos ativos do inimigo ao ser derrotado
        if hasattr(inimigo, 'efeitos_ativos'):
            inimigo.efeitos_ativos = {}

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

    def _aplicar_efeitos_inimigo(self, inimigo):
        # Este método será chamado no turno do inimigo para aplicar efeitos como veneno
        if not hasattr(inimigo, 'efeitos_ativos'):
            return

        efeitos_para_remover = []
        for efeito_nome, dados_efeito in inimigo.efeitos_ativos.items():
            if dados_efeito['tipo'] == 'dano_por_turno':
                dano_efeito = dados_efeito['valor']
                inimigo.vida -= dano_efeito
                self.log_mensagem(f"{inimigo.tipo} sofre {dano_efeito} de dano de {efeito_nome}!")
            elif dados_efeito['tipo'] == 'debuff_precisao':
                # A precisão já foi reduzida quando o debuff foi aplicado.
                # Aqui apenas decrementamos o contador de turnos.
                pass
            # Adicione outros tipos de efeitos de inimigo aqui

            dados_efeito['turnos_restantes'] -= 1
            if dados_efeito['turnos_restantes'] <= 0:
                efeitos_para_remover.append(efeito_nome)
                # Reverter o efeito quando ele expira
                if dados_efeito['tipo'] == 'debuff_precisao':
                    inimigo.precisao += dados_efeito['valor']
                    self.log_mensagem(f"O efeito de {efeito_nome} no {inimigo.tipo} terminou. Precisão restaurada.")

        for efeito_nome in efeitos_para_remover:
            del inimigo.efeitos_ativos[efeito_nome]

    def aplicar_habilidade(self, habilidade_nome):
        # Obtém os dados da habilidade do dicionário do jogador
        # que já contém o 'efeito_combate'
        habilidade_data = self.player.habilidades.get(habilidade_nome)

        if not habilidade_data:
            self.log_mensagem("Habilidade desconhecida!")
            return "combate" # Retorna para o combate se a habilidade não for encontrada

        efeito_combate_str = habilidade_data['efeito_combate']

        if efeito_combate_str in self.efeito_combate_map:
            # Chama o método correspondente à string de efeito
            self.efeito_combate_map[efeito_combate_str]()
        else:
            self.log_mensagem("Lógica para esta habilidade não implementada!")
            return "combate"

        # Lógica de pós-habilidade (verificação de vida do inimigo e contra-ataque)
        inimigo = self.current_enemy
        jogador = self.player

        if inimigo.vida <= 0:
            return self._derrotar_inimigo(inimigo)
        else:
            # Aplica efeitos de status do inimigo (se houver)
            self._aplicar_efeitos_inimigo(inimigo)

            # Inimigo contra-ataca após a habilidade, a menos que a habilidade seja de cura/buff/debuff
            # ou já tenha lidado com o contra-ataque (como Ataque Básico)
            habilidade_tipo = habilidade_data['tipo']
            # O inimigo só contra-ataca se a habilidade for de dano e não for o Ataque Básico
            if habilidade_tipo in ['dano', 'dano_cura', 'dano_debuff'] and habilidade_nome != 'Ataque Básico':
                acertou_inimigo, chance_inimigo = self._calcular_acerto(inimigo, jogador)
                if acertou_inimigo:
                    dano_inimigo = max(1, inimigo.ataque - jogador.defesa // 2)
                    jogador.vida -= dano_inimigo
                    self.log_mensagem(f"{inimigo.tipo} contra-atacou causando {dano_inimigo} de dano! (Chance: {chance_inimigo}%)")
                else:
                    self.log_mensagem(f"{inimigo.tipo} errou o ataque! (Chance: {chance_inimigo}%)")

            if jogador.vida <= 0:
                self.game_over()
                return "game_over"
            return "combate"

    # --- Métodos de Aplicação de Habilidades ---
    # Estes métodos são chamados pelo self.efeito_combate_map

    def _aplicar_ataque_basico(self):
        return self.resolver_combate_acao('atacar')

    def _aplicar_golpe_poderoso(self):
        inimigo = self.current_enemy
        jogador = self.player
        acertou_jogador, chance_jogador = self._calcular_acerto(jogador, inimigo)
        if acertou_jogador:
            dano = max(1, jogador.ataque * 2 - inimigo.defesa // 2)
            inimigo.vida -= dano
            self.log_mensagem(f"Golpe Poderoso! Causou {dano} de dano! (Chance: {chance_jogador}%)")
        else:
            self.log_mensagem(f"Golpe Poderoso errou! (Chance: {chance_jogador}%)")

    def _aplicar_bola_de_fogo(self):
        inimigo = self.current_enemy
        jogador = self.player
        acertou_jogador, chance_jogador = self._calcular_acerto(jogador, inimigo)
        if acertou_jogador:
            dano = max(1, jogador.ataque * 3 - inimigo.defesa // 4)
            inimigo.vida -= dano
            self.log_mensagem(f"Bola de Fogo! Causou {dano} de dano! (Chance: {chance_jogador}%)")
        else:
            self.log_mensagem(f"Bola de Fogo errou! (Chance: {chance_jogador}%)")

    def _aplicar_chuva_de_flechas(self):
        inimigo = self.current_enemy
        jogador = self.player
        acertou_jogador, chance_jogador = self._calcular_acerto(jogador, inimigo)
        if acertou_jogador:
            dano = max(1, jogador.ataque * 1.5 - inimigo.defesa // 3)
            inimigo.vida -= dano
            self.log_mensagem(f"Chuva de Flechas! Causou {dano} de dano! (Chance: {chance_jogador}%)")
        else:
            self.log_mensagem(f"Chuva de Flechas errou! (Chance: {chance_jogador}%)")

    def _aplicar_golpe_critico(self):
        inimigo = self.current_enemy
        jogador = self.player
        self.log_mensagem("Você prepara um Golpe Crítico!")
        acertou_jogador, chance_jogador = self._calcular_acerto(jogador, inimigo)
        if acertou_jogador and random.random() < 0.7:
            dano = max(1, jogador.ataque * 2.5 - inimigo.defesa // 2)
            inimigo.vida -= dano
            self.log_mensagem(f"Golpe Crítico acertou! Causou {dano} de dano! (Chance: {chance_jogador}%)")
        else:
            self.log_mensagem(f"Golpe Crítico falhou ou errou! (Chance: {chance_jogador}%)")

    def _aplicar_ataque_duplo(self):
        inimigo = self.current_enemy
        jogador = self.player
        total_dano = 0
        acertou_primeiro, chance_primeiro = self._calcular_acerto(jogador, inimigo)
        if acertou_primeiro:
            dano1 = max(1, jogador.ataque - inimigo.defesa // 2)
            total_dano += dano1
            self.log_mensagem(f"Primeiro ataque acertou! Causou {dano1} de dano! (Chance: {chance_primeiro}%)")
        else:
            self.log_mensagem(f"Primeiro ataque errou! (Chance: {chance_primeiro}%)")

        acertou_segundo, chance_segundo = self._calcular_acerto(jogador, inimigo)
        if acertou_segundo:
            dano2 = max(1, jogador.ataque - inimigo.defesa // 2)
            total_dano += dano2
            self.log_mensagem(f"Segundo ataque acertou! Causou {dano2} de dano! (Chance: {chance_segundo}%)")
        else:
            self.log_mensagem(f"Segundo ataque errou! (Chance: {chance_segundo}%)")
        inimigo.vida -= total_dano
        self.log_mensagem(f"Ataque Duplo totalizou {total_dano} de dano!")

    def _aplicar_ataque_rapido(self):
        inimigo = self.current_enemy
        jogador = self.player
        acertou_jogador, chance_jogador = self._calcular_acerto(jogador, inimigo)
        if acertou_jogador:
            dano = max(1, jogador.ataque * 1.2 - inimigo.defesa // 2)
            inimigo.vida -= dano
            self.log_mensagem(f"Ataque Rápido! Causou {dano} de dano! (Chance: {chance_jogador}%)")
        else:
            self.log_mensagem(f"Ataque Rápido errou! (Chance: {chance_jogador}%)")

    def _aplicar_ataque_furtivo(self):
        inimigo = self.current_enemy
        jogador = self.player
        acertou_jogador, chance_jogador = self._calcular_acerto(jogador, inimigo)
        if acertou_jogador:
            dano = max(1, jogador.ataque * 2.8 - inimigo.defesa // 2)
            inimigo.vida -= dano
            self.log_mensagem(f"Ataque Furtivo! Causou {dano} de dano! (Chance: {chance_jogador}%)")
        else:
            self.log_mensagem(f"Ataque Furtivo errou! (Chance: {chance_jogador}%)")

    def _aplicar_ataque_giratorio(self):
        inimigo = self.current_enemy
        jogador = self.player
        acertou_jogador, chance_jogador = self._calcular_acerto(jogador, inimigo)
        if acertou_jogador:
            dano = max(1, jogador.ataque * 1.8 - inimigo.defesa // 2)
            inimigo.vida -= dano
            self.log_mensagem(f"Ataque Giratório! Causou {dano} de dano! (Chance: {chance_jogador}%)")
        else:
            self.log_mensagem(f"Ataque Giratório errou! (Chance: {chance_jogador}%)")

    def _aplicar_cura_rapida(self):
        jogador = self.player
        cura = 25
        jogador.vida = min(jogador.vida + cura, jogador.vida_max)
        self.log_mensagem(f"Cura Rápida! Recuperou {cura} de vida!")

    def _aplicar_cura_leve(self):
        jogador = self.player
        cura = 40
        jogador.vida = min(jogador.vida + cura, jogador.vida_max)
        self.log_mensagem(f"Cura Leve! Recuperou {cura} de vida!")

    def _aplicar_cura_menor(self):
        jogador = self.player
        cura = 20
        jogador.vida = min(jogador.vida + cura, jogador.vida_max)
        self.log_mensagem(f"Cura Menor! Recuperou {cura} de vida!")

    def _aplicar_foco_preciso(self):
        jogador = self.player
        if 'Foco Preciso' not in jogador.efeitos_ativos:
            jogador.precisao += 15
            jogador.efeitos_ativos['Foco Preciso'] = {'turnos_restantes': 3, 'valor': 15, 'tipo': 'buff_precisao'}
            self.log_mensagem("Você usou Foco Preciso! Sua precisão aumentou em 15 por 3 turnos!")
        else:
            self.log_mensagem("Foco Preciso já está ativo!")

    def _aplicar_pele_de_pedra(self):
        jogador = self.player
        if 'Pele de Pedra' not in jogador.efeitos_ativos:
            jogador.defesa += 7
            jogador.efeitos_ativos['Pele de Pedra'] = {'turnos_restantes': 4, 'valor': 7, 'tipo': 'buff_defesa'}
            self.log_mensagem("Você usou Pele de Pedra! Sua defesa aumentou em 7 por 4 turnos!")
        else:
            self.log_mensagem("Pele de Pedra já está ativo!")

    def _aplicar_escudo_divino(self):
        jogador = self.player
        if 'Escudo Divino' not in jogador.efeitos_ativos:
            jogador.defesa += 10
            jogador.efeitos_ativos['Escudo Divino'] = {'turnos_restantes': 2, 'valor': 10, 'tipo': 'buff_defesa'}
            self.log_mensagem("Você invocou um Escudo Divino! Sua defesa aumentou em 10 por 2 turnos!")
        else:
            self.log_mensagem("Escudo Divino já está ativo!")

    # --- Novas Habilidades ---

    def _aplicar_investida_brutal(self):
        inimigo = self.current_enemy
        jogador = self.player
        acertou_jogador, chance_jogador = self._calcular_acerto(jogador, inimigo)
        if acertou_jogador:
            dano = max(1, jogador.ataque * 2.2 - inimigo.defesa // 2)
            inimigo.vida -= dano
            self.log_mensagem(f"Investida Brutal! Causou {dano} de dano! (Chance: {chance_jogador}%)")
            if random.random() < 0.2: # 20% chance de atordoar
                if 'Atordoado' not in inimigo.efeitos_ativos:
                    inimigo.efeitos_ativos['Atordoado'] = {'turnos_restantes': 1, 'tipo': 'atordoado'}
                    self.log_mensagem(f"{inimigo.tipo} está atordoado por 1 turno!")
                else:
                    self.log_mensagem(f"{inimigo.tipo} já está atordoado!")
        else:
            self.log_mensagem(f"Investida Brutal errou! (Chance: {chance_jogador}%)")

    def _aplicar_raio_arcano(self):
        inimigo = self.current_enemy
        jogador = self.player
        acertou_jogador, chance_jogador = self._calcular_acerto(jogador, inimigo)
        if acertou_jogador:
            dano = max(1, jogador.ataque * 2.5 - inimigo.defesa // 3)
            inimigo.vida -= dano
            self.log_mensagem(f"Raio Arcano! Causou {dano} de dano! (Chance: {chance_jogador}%)")
        else:
            self.log_mensagem(f"Raio Arcano errou! (Chance: {chance_jogador}%)")

    def _aplicar_tiro_multiplo(self):
        inimigo = self.current_enemy
        jogador = self.player
        total_dano = 0
        num_flechas = 3
        self.log_mensagem("Você dispara uma saraivada de flechas!")
        for i in range(num_flechas):
            acertou_jogador, chance_jogador = self._calcular_acerto(jogador, inimigo)
            if acertou_jogador:
                dano_flecha = max(1, (jogador.ataque * 0.7) - inimigo.defesa // 4)
                total_dano += dano_flecha
                self.log_mensagem(f"  Flecha {i+1} acertou! Causou {int(dano_flecha)} de dano!")
            else:
                self.log_mensagem(f"  Flecha {i+1} errou!")
        inimigo.vida -= total_dano
        self.log_mensagem(f"Tiro Múltiplo totalizou {int(total_dano)} de dano!")

    def _aplicar_distracao(self):
        inimigo = self.current_enemy
        # Reduz a precisão do inimigo temporariamente
        if 'Distração' not in inimigo.efeitos_ativos:
            debuff_valor = 15
            inimigo.precisao = max(0, inimigo.precisao - debuff_valor)
            inimigo.efeitos_ativos['Distração'] = {'turnos_restantes': 2, 'valor': debuff_valor, 'tipo': 'debuff_precisao'}
            self.log_mensagem(f"Você distraiu o {inimigo.tipo}! A precisão dele diminuiu em {debuff_valor} por 2 turnos!")
        else:
            self.log_mensagem(f"{inimigo.tipo} já está distraído!")

    def _aplicar_bencao_divina(self):
        jogador = self.player
        if 'Bênção Divina' not in jogador.efeitos_ativos:
            buff_defesa = 5
            cura = 20
            jogador.defesa += buff_defesa
            jogador.vida = min(jogador.vida + cura, jogador.vida_max)
            jogador.efeitos_ativos['Bênção Divina'] = {'turnos_restantes': 3, 'valor': buff_defesa, 'tipo': 'buff_defesa'}
            self.log_mensagem(f"Você recebeu uma Bênção Divina! Recuperou {cura} de vida e sua defesa aumentou em {buff_defesa} por 3 turnos!")
        else:
            self.log_mensagem("Bênção Divina já está ativa!")

    def _aplicar_drenar_vida(self):
        inimigo = self.current_enemy
        jogador = self.player
        acertou_jogador, chance_jogador = self._calcular_acerto(jogador, inimigo)
        if acertou_jogador:
            dano = max(1, jogador.ataque * 1.0 - inimigo.defesa // 2)
            cura = int(dano * 0.5)
            inimigo.vida -= dano
            jogador.vida = min(jogador.vida + cura, jogador.vida_max)
            self.log_mensagem(f"Drenar Vida! Causou {dano} de dano e recuperou {cura} de vida! (Chance: {chance_jogador}%)")
        else:
            self.log_mensagem(f"Drenar Vida errou! (Chance: {chance_jogador}%)")

    def _aplicar_ataque_venenoso(self): # Nova habilidade
        inimigo = self.current_enemy
        jogador = self.player
        acertou_jogador, chance_jogador = self._calcular_acerto(jogador, inimigo)
        if acertou_jogador:
            dano = max(1, jogador.ataque * 1.3 - inimigo.defesa // 2)
            inimigo.vida -= dano
            self.log_mensagem(f"Ataque Venenoso! Causou {dano} de dano! (Chance: {chance_jogador}%)")

            if 'Veneno' not in inimigo.efeitos_ativos:
                dano_veneno_por_turno = 5 + int(jogador.nivel / 5) # Escala com o nível
                inimigo.efeitos_ativos['Veneno'] = {'turnos_restantes': 3, 'valor': dano_veneno_por_turno, 'tipo': 'dano_por_turno'}
                self.log_mensagem(f"{inimigo.tipo} foi envenenado! Sofrerá {dano_veneno_por_turno} de dano por 3 turnos.")
            else:
                self.log_mensagem(f"{inimigo.tipo} já está envenenado!")
        else:
            self.log_mensagem(f"Ataque Venenoso errou! (Chance: {chance_jogador}%)")

    def _aplicar_grito_de_guerra(self): # Nova habilidade
        jogador = self.player
        if 'Grito de Guerra' not in jogador.efeitos_ativos:
            buff_ataque = 7
            jogador.ataque += buff_ataque
            jogador.efeitos_ativos['Grito de Guerra'] = {'turnos_restantes': 3, 'valor': buff_ataque, 'tipo': 'buff_ataque'}
            self.log_mensagem(f"Você soltou um Grito de Guerra! Seu ataque aumentou em {buff_ataque} por 3 turnos!")
        else:
            self.log_mensagem("Grito de Guerra já está ativo!")

    def _aplicar_escudo_de_mana(self): # Nova habilidade
        jogador = self.player
        if 'Escudo de Mana' not in jogador.efeitos_ativos:
            escudo_valor = 30 + (jogador.nivel * 2) # Escala com o nível
            # Para um escudo que absorve dano, precisaríamos de um atributo temporário de "escudo" no jogador
            # Por simplicidade, vamos fazer com que ele dê um buff de defesa muito alto por 1 turno.
            jogador.defesa += escudo_valor # Aumenta defesa drasticamente
            jogador.efeitos_ativos['Escudo de Mana'] = {'turnos_restantes': 1, 'valor': escudo_valor, 'tipo': 'buff_defesa'}
            self.log_mensagem(f"Você conjurou um Escudo de Mana! Sua defesa aumentou em {escudo_valor} por 1 turno!")
        else:
            self.log_mensagem("Escudo de Mana já está ativo!")


    def usar_item_combate(self, item_nome):
        if self.player.inventario.get(item_nome, 0) > 0:
            self.player.usar_item(item_nome, self.log_mensagem)
            # Inimigo ataca após o uso do item
            inimigo = self.current_enemy
            jogador = self.player

            # Aplica efeitos de status do inimigo (se houver)
            self._aplicar_efeitos_inimigo(inimigo)

            acertou_inimigo, chance_inimigo = self._calcular_acerto(inimigo, jogador)
            if acertou_inimigo:
                dano_inimigo = max(1, inimigo.ataque - jogador.defesa // 2)
                jogador.vida -= dano_inimigo
                self.log_mensagem(f"{inimigo.tipo} atacou causando {dano_inimigo} de dano! (Chance: {chance_inimigo}%)")
            else:
                self.log_mensagem(f"{inimigo.tipo} errou o ataque! (Chance: {chance_inimigo}%)")

            if jogador.vida <= 0:
                self.game_over()
                return "game_over"
            return "combate"
        else:
            self.log_mensagem("Você não tem este item!")
            return "combate"

