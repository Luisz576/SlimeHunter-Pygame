class PlayerInventory:
    def __init__(self, max_arrows):
        self.max_arrows = max_arrows
        self._arrows = 0

    def arrows(self):
        return self._arrows

    def give_arrow(self):
        self._arrows = min(self._arrows + 1, self.max_arrows)

    def use_arrow(self):
        self._arrows = max(0, self._arrows - 1)
