class Enemy:
    def __init__(self, tipo, vida, ataque, defesa, xp, ouro, chefao=False):
        self.tipo = tipo
        self.vida = vida
        self.vida_max = vida
        self.ataque = ataque
        self.defesa = defesa
        self.xp = xp
        self.ouro = ouro
        self.chefao = chefao
        self.x = 0
        self.y = 0

    def __repr__(self):
        return f"{self.tipo} (Vida: {self.vida}/{self.vida_max})"

