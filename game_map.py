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

        tem_chefao = self.dungeon_nivel % 5 == 0

        tipos_inimigos_data = [
            {'tipo': 'Goblin', 'vida': 20, 'ataque': 8, 'defesa': 3, 'xp': 15, 'ouro': 10},
            {'tipo': 'Esqueleto', 'vida': 30, 'ataque': 10, 'defesa': 5, 'xp': 25, 'ouro': 15},
            {'tipo': 'Orc', 'vida': 50, 'ataque': 15, 'defesa': 8, 'xp': 40, 'ouro': 25},
            {'tipo': 'Morto-Vivo', 'vida': 35, 'ataque':12, 'defesa':2, 'xp':30, 'ouro': 22},
            {'tipo': 'Slime', 'vida':100, 'ataque': 3, 'defesa': 1, 'xp':17, 'ouro':0}
        ]

        if tem_chefao:
            chefao_data = {
                'tipo': 'DRAGÃO',
                'vida': 100 * self.dungeon_nivel,
                'ataque': 20 * self.dungeon_nivel,
                'defesa': 15 * self.dungeon_nivel,
                'xp': 200 * self.dungeon_nivel,
                'ouro': 100 * self.dungeon_nivel,
                'chefao': True
            }
            self.inimigos.append(self._criar_entidade(Enemy, chefao_data, forcado=True))

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
        while True:
            if x is None or y is None:
                pos_x, pos_y = random.randint(1, self.largura-2), random.randint(1, self.altura-2)
            else:
                pos_x, pos_y = x, y

            pos_valida = (
                self.mapa[pos_y][pos_x] == '.' and
                not any(e.x == pos_x and e.y == pos_y for e in self.inimigos) and
                not any(i.x == pos_x and i.y == pos_y for i in self.itens) and
                not any(n.x == pos_x and n.y == pos_y for n in self.npcs) or
                forcado
            )

            if pos_valida:
                if entity_class == Enemy:
                    entidade = Enemy(dados['tipo'], dados['vida'], dados['ataque'], dados['defesa'], dados['xp'], dados['ouro'], dados.get('chefao', False))
                elif entity_class == Item:
                    entidade = Item(dados['tipo'], dados.get('quantidade', 1), dados.get('efeito'))
                elif entity_class == NPC:
                    entidade = NPC(dados['tipo'], dados['dialogo'])
                else:
                    raise ValueError("Tipo de entidade desconhecido")

                entidade.x = pos_x
                entidade.y = pos_y
                return entidade

    def get_entities_at_position(self, x, y):
        inimigo = next((e for e in self.inimigos if e.x == x and e.y == y), None)
        item = next((i for i in self.itens if i.x == x and i.y == y), None)
        portal = next((p for p in self.portais if p['x'] == x and p['y'] == y), None)
        npc = next((n for n in self.npcs if n.x == x and n.y == y), None)
        return inimigo, item, portal, npc

    def remove_entity(self, entity):
        """Remove uma entidade (inimigo, item, etc.) do mapa"""
        if isinstance(entity, Enemy):
            if entity in self.inimigos:
             self.inimigos.remove(entity)
        elif isinstance(entity, Item):
            if entity in self.itens:
             self.itens.remove(entity)
