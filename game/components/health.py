class Health:
    def __init__(self, max_health):
        self.max_health = max_health
        self.health = max_health

    def hurt(self, damage):
        self.health = self.health - damage

    def heal(self, heal):
        self.health = self.health + heal
