from Cards.Card import Card


class DistrictCard(Card):
    def __init__(self, name: str):
        super().__init__(name)
        self.name = None
        self.cost = 0
