# entities/enemy.py

class Enemy:
    def __init__(self, tipo, vida, ataque, defesa, xp, ouro, chefao=False, is_miniboss=False, precisao=80, esquiva=5):
        self.tipo = tipo
        self.vida = vida
        self.vida_max = vida
        self.ataque = ataque
        self.defesa = defesa
        self.xp = xp
        self.ouro = ouro
        self.chefao = chefao
        self.is_miniboss = is_miniboss
        self.x = 0
        self.y = 0
        self.precisao = precisao # Precisão do inimigo
        self.esquiva = esquiva   # Esquiva do inimigo
        self.efeitos_ativos = {} # NOVO: Dicionário para efeitos temporários no inimigo

    def __repr__(self):
        return f"{self.tipo} (Vida: {self.vida}/{self.vida_max})"

