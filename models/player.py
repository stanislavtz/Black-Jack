from models.table import Table


class Player(Table):
    def __init__(self, name):
        super().__init__()
        self.name = name
