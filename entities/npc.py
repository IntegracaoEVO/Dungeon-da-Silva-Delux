class NPC:
    def __init__(self, tipo, dialogo):
        self.tipo = tipo
        self.dialogo = dialogo
        self.x = 0
        self.y = 0

    def __repr__(self):
        return f"{self.tipo}"

