class Health:
    def __init__(self, max_health):
        self.max_health = max_health
        self.health = max_health

    def hurt(self, damage):
        self.health = max(self.health - damage, 0)

    def heal(self, heal):
        self.health = min(self.health + heal, self.max_health)
