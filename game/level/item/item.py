class Item:
    def __init__(self, id, name, sprite_path, amount=1):
        self.id = id
        self.name = name
        self.amount = amount
        self.sprite_path = sprite_path