from game.level import Level


class MenuLevel(Level):
    def __init__(self):
        super().__init__()

    def run(self, delta):
        self.render()

    def render(self):
        # TODO: titulo game e botões
        pass
