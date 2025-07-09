from entities.item import Item

class ShopSystem:
    def __init__(self, player, log_callback):
        self.player = player
        self.log_mensagem = log_callback
        self.loja_itens = [
            Item(nome='Poção de Vida', preco=20, tipo='consumivel', efeito='cura 30'),
            Item(nome='Poção de Ataque', preco=30, tipo='consumivel', efeito='ataque +5'),
            Item(nome='Espada de Ferro', preco=100, tipo='equipamento', ataque=5),
            Item(nome='Cajado velho', preco=250, tipo='equipamento', ataque=8),
            Item(nome='Armadura de Couro', preco=80, tipo='equipamento', defesa=3)
        ]

    def comprar_item(self, item_idx):
    # Verifica se o índice é válido
        if item_idx < 0 or item_idx >= len(self.loja_itens):
            self.log_mensagem("Item inválido!")
            return

        item = self.loja_itens[item_idx]

        if self.player.ouro >= item.preco:
            self.player.ouro -= item.preco
            self.player.inventario[item.nome] = self.player.inventario.get(item.nome, 0) + 1
            self.log_mensagem(f"Comprou {item.nome} por {item.preco} de ouro!")
            
            # Aplica efeitos de equipamento (se for o caso)
            if item.tipo == 'equipamento':
                if item.ataque:
                    self.player.ataque += item.ataque
                if item.defesa:
                    self.player.defesa += item.defesa
                self.log_mensagem(f"{item.nome} equipado! Atributos atualizados.")
        else:
            self.log_mensagem("Ouro insuficiente!")
