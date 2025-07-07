class Item:
    def __init__(self, tipo, quantidade=1, efeito=None, nome=None, preco=None, ataque=None, defesa=None):
        self.tipo = tipo
        self.quantidade = quantidade
        self.efeito = efeito
        self.nome = nome if nome else tipo # Para itens da loja
        self.preco = preco
        self.ataque = ataque
        self.defesa = defesa
        self.x = 0
        self.y = 0

    def __repr__(self):
        return f"{self.tipo} (Qtd: {self.quantidade})"

