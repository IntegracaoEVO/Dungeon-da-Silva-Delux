# game_map.py
import random
from entities.enemy import Enemy
from entities.item import Item
from entities.npc import NPC

class GameMap:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.mapa = []
        self.inimigos = []
        self.itens = []
        self.portais = []
        self.npcs = []
        self.dungeon_nivel = 1

    def gerar_dungeon(self, player_ref):
        self.mapa = [['#' for _ in range(self.largura)] for _ in range(self.altura)]
        salas = []

        for _ in range(5 + self.dungeon_nivel):
            sala = {
                'x': random.randint(1, self.largura - 10),
                'y': random.randint(1, self.altura - 6),
                'largura': random.randint(5, 10),
                'altura': random.randint(4, 6)
            }
            salas.append(sala)

            for y in range(sala['y'], sala['y'] + sala['altura']):
                for x in range(sala['x'], sala['x'] + sala['largura']):
                    if 0 <= x < self.largura and 0 <= y < self.altura:
                        self.mapa[y][x] = '.'

        for i in range(len(salas)-1):
            self._conectar_salas(salas[i], salas[i+1])

        sala_inicial = salas[0]
        player_ref.x = sala_inicial['x'] + 1
        player_ref.y = sala_inicial['y'] + 1

        self._gerar_entidades(salas)

    def _conectar_salas(self, sala1, sala2):
        x1, y1 = sala1['x'] + sala1['largura']//2, sala1['y'] + sala1['altura']//2
        x2, y2 = sala2['x'] + sala2['largura']//2, sala2['y'] + sala2['altura']//2

        for x in range(min(x1, x2), max(x1, x2)+1):
            if 0 <= x < self.largura and 0 <= y1 < self.altura:
                self.mapa[y1][x] = '.'

        for y in range(min(y1, y2), max(y1, y2)+1):
            if 0 <= x2 < self.largura and 0 <= y < self.altura:
                self.mapa[y][x2] = '.'

    def _gerar_entidades(self, salas):

        self.inimigos = []
        self.itens = []
        self.portais = []
        self.npcs = []

        tem_chefao_principal = self.dungeon_nivel % 5 == 0
        fator_poder = 1 + (self.dungeon_nivel * 0.3)
        tem_mini_chefao = self.dungeon_nivel % 2 == 0 and not tem_chefao_principal

        inimigos_base = [
            {'tipo': 'Goblin', 'vida': 20, 'ataque': 8, 'defesa': 3, 'xp': 15, 'ouro': 10, 'precisao': 70, 'esquiva': 5},
            {'tipo': 'Esqueleto', 'vida': 30, 'ataque': 10, 'defesa': 5, 'xp': 25, 'ouro': 15, 'precisao': 75, 'esquiva': 8},
            {'tipo': 'Orc', 'vida': 50, 'ataque': 15, 'defesa': 8, 'xp': 40, 'ouro': 25, 'precisao': 80, 'esquiva': 10},
            {'tipo': 'Morto-Vivo', 'vida': 35, 'ataque':12, 'defesa':2, 'xp':30, 'ouro': 22, 'precisao': 65, 'esquiva': 3},
            {'tipo': 'Slime', 'vida':100, 'ataque': 3, 'defesa': 1, 'xp':17, 'ouro':0, 'precisao': 50, 'esquiva': 0}
        ]

        tipos_inimigos_data = []
        for inimigo in inimigos_base:
            inimigo_escalado = inimigo.copy()
            for atributo in ['vida', 'ataque', 'defesa', 'xp', 'ouro']:
                inimigo_escalado[atributo] = int(inimigo[atributo] * fator_poder)
            # Escalonamento de precisão e esquiva pode ser mais suave
            inimigo_escalado['precisao'] = int(inimigo['precisao'] * (1 + (self.dungeon_nivel * 0.05)))
            inimigo_escalado['esquiva'] = int(inimigo['esquiva'] * (1 + (self.dungeon_nivel * 0.05)))
            tipos_inimigos_data.append(inimigo_escalado)

        tipos_mini_chefes_data = [
            {'tipo': 'Ogro', 'vida': 200, 'ataque': 20, 'defesa': 10, 'xp': 70, 'ouro': 50, 'is_miniboss': True, 'precisao': 85, 'esquiva': 15},
            {'tipo': 'Lich', 'vida': 85, 'ataque': 30, 'defesa': 8, 'xp': 80, 'ouro': 60, 'is_miniboss': True, 'precisao': 90, 'esquiva': 20}
        ]
        # Escalonar mini-chefes
        for mini_chefao in tipos_mini_chefes_data:
            for atributo in ['vida', 'ataque', 'defesa', 'xp', 'ouro']:
                mini_chefao[atributo] = int(mini_chefao[atributo] * fator_poder)
            mini_chefao['precisao'] = int(mini_chefao['precisao'] * (1 + (self.dungeon_nivel * 0.05)))
            mini_chefao['esquiva'] = int(mini_chefao['esquiva'] * (1 + (self.dungeon_nivel * 0.05)))


        chefao_principal_data = {
            'tipo': 'Fantasma de Dragão',
            'vida': 350 * self.dungeon_nivel,
            'ataque': 20 * self.dungeon_nivel,
            'defesa': 12 * self.dungeon_nivel,
            'xp': 200 * self.dungeon_nivel,
            'ouro': 100 * self.dungeon_nivel,
            'chefao': True,
            'precisao': 95,
            'esquiva': 25
        }
        # Escalonar chefão principal
        chefao_principal_data['precisao'] = int(chefao_principal_data['precisao'] * (1 + (self.dungeon_nivel * 0.05)))
        chefao_principal_data['esquiva'] = int(chefao_principal_data['esquiva'] * (1 + (self.dungeon_nivel * 0.05)))


        if tem_chefao_principal:
            self.inimigos.append(self._criar_entidade(Enemy, chefao_principal_data, forcado=True))
        elif tem_mini_chefao:
            mini_chefao_data = random.choice(tipos_mini_chefes_data)
            self.inimigos.append(self._criar_entidade(Enemy, mini_chefao_data, forcado=True))

        for _ in range(5 + self.dungeon_nivel * 2):
            tipo_data = random.choice(tipos_inimigos_data)
            self.inimigos.append(self._criar_entidade(Enemy, tipo_data))

        tipos_itens_data = [
            {'tipo': 'Poção de Vida', 'quantidade': 1},
            {'tipo': 'Poção de Ataque', 'quantidade': 1},
            {'tipo': 'Ouro', 'quantidade': random.randint(5, 20) * self.dungeon_nivel},
            {'tipo': 'Pergaminho', 'quantidade': 1, 'efeito': 'habilidade'}
        ]

        for _ in range(3 + self.dungeon_nivel):
            item_data = random.choice(tipos_itens_data)
            self.itens.append(self._criar_entidade(Item, item_data))

        ultima_sala = salas[-1]
        portal = {
            'x': ultima_sala['x'] + ultima_sala['largura']//2,
            'y': ultima_sala['y'] + ultima_sala['altura']//2,
            'tipo': 'Portal'
        }
        self.portais.append(portal)

        if random.random() < 0.3:
            mercador_data = {
                'tipo': 'Mercador',
                'dialogo': "Compre meus itens raros! (L para acessar loja)"
            }
            self.npcs.append(self._criar_entidade(NPC, mercador_data, x=salas[1]['x'] + 1, y=salas[1]['y'] + 1))

    def _criar_entidade(self, entity_class, dados, forcado=False, x=None, y=None):
        tentativas = 0
        max_tentativas = 100

        while tentativas < max_tentativas:
            if x is None or y is None:
                pos_x = random.randint(1, self.largura - 2)
                pos_y = random.randint(1, self.altura - 2)
            else:
                pos_x, pos_y = x, y

            is_ground = self.mapa[pos_y][pos_x] == '.'
            has_other_entity = (
                any(e.x == pos_x and e.y == pos_y for e in self.inimigos) or
                any(i.x == pos_x and i.y == pos_y for i in self.itens) or
                any(n.x == pos_x and n.y == pos_y for n in self.npcs)
            )

            pos_valida = is_ground and (not has_other_entity or forcado)

            if pos_valida:
                if entity_class == Enemy:
                    entidade = Enemy(
                        dados['tipo'], dados['vida'], dados['ataque'],
                        dados['defesa'], dados['xp'], dados['ouro'],
                        dados.get('chefao', False), dados.get('is_miniboss', False),
                        dados.get('precisao', 80), dados.get('esquiva', 5)
                    )
                elif entity_class == Item:
                    entidade = Item(dados['tipo'], dados.get('quantidade', 1), dados.get('efeito'))
                elif entity_class == NPC:
                    entidade = NPC(dados['tipo'], dados['dialogo'])
                else:
                    raise ValueError("Tipo de entidade desconhecido")

                entidade.x = pos_x
                entidade.y = pos_y
                return entidade

            tentativas += 1

        print(f"[AVISO] Não foi possível gerar {dados['tipo']} em posição válida após {max_tentativas} tentativas!")
        return None

    def get_entities_at_position(self, x, y):
        inimigo = next((e for e in self.inimigos if e.x == x and e.y == y), None)
        item = next((i for i in self.itens if i.x == x and i.y == y), None)
        portal = next((p for p in self.portais if p['x'] == x and p['y'] == y), None)
        npc = next((n for n in self.npcs if n.x == x and n.y == y), None)
        return inimigo, item, portal, npc

    def remove_entity(self, entity):
        if isinstance(entity, Enemy):
            if entity in self.inimigos:
             self.inimigos.remove(entity)
        elif isinstance(entity, Item):
            if entity in self.itens:
             self.itens.remove(entity)
