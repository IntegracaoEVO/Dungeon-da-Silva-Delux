# systems/shop_system.py
from entities.item import Item

class ShopSystem:
    def __init__(self, player, log_callback, game_map_ref): # Adicione game_map_ref
        self.player = player
        self.log_mensagem = log_callback
        self.game_map_ref = game_map_ref # Armazena a referência do mapa
        self.loja_itens = self._gerar_itens_loja() # Chama um método para gerar itens

    def _gerar_itens_loja(self):
        dungeon_nivel_atual = self.game_map_ref.dungeon_nivel if self.game_map_ref else 1
        fator_preco = 1 + (dungeon_nivel_atual * 0.1) # Ajuste o fator conforme desejar

        return [
            Item(nome='Poção de Vida', preco=int(20 * fator_preco), tipo='consumivel', efeito='cura 30'),
            Item(nome='Poção de Ataque', preco=int(30 * fator_preco), tipo='consumivel', efeito='ataque +5'),
            Item(nome='Espada de Ferro', preco=int(100 * fator_preco), tipo='equipamento', ataque=5),
            Item(nome='Cajado velho', preco=int(250 * fator_preco), tipo='equipamento', ataque=8),
            Item(nome='Armadura de Couro', preco=int(80 * fator_preco), tipo='equipamento', defesa=3)
        ]

    def atualizar_loja(self):
        self.loja_itens = self._gerar_itens_loja()
        self.log_mensagem("Os itens da loja foram atualizados!")

    def comprar_item(self, item_idx):
        if item_idx < 0 or item_idx >= len(self.loja_itens):
            self.log_mensagem("Item inválido!")
            return

        item = self.loja_itens[item_idx]

        if self.player.ouro >= item.preco:
            self.player.ouro -= item.preco
            self.player.inventario[item.nome] = self.player.inventario.get(item.nome, 0) + 1
            self.log_mensagem(f"Comprou {item.nome} por {item.preco} de ouro!")

            if item.tipo == 'equipamento':
                if item.ataque:
                    self.player.ataque += item.ataque
                if item.defesa:
                    self.player.defesa += item.defesa
                self.log_mensagem(f"{item.nome} equipado! Atributos atualizados.")
        else:
            self.log_mensagem("Ouro insuficiente!")
