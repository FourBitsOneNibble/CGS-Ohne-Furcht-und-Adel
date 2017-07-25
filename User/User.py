from abc import ABC, abstractmethod

from Logic import Logic
from Player import Player


class User(ABC):
    def __init__(self, logic: Logic):
        self.player = Player()
        self.setLogic(logic)

    def setLogic(self, logic: Logic):
        self.logic = logic
        self.logic.bind('<<events>>', self.playerEvents)

    @abstractmethod
    def playerEvents(self, *args, **kv):
        pass

if __name__ == '__main__':
    user = User()
    user.setLogic(Logic())
    user.logic.addPlayer(user.player)
    user.logic.startGame()
    user.logic.endTurn(user.player)
