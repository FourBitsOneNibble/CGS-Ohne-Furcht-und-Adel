from typing import List

from Cards.CharacterCards import CharacterCard
from Cards.DistrictCards.DistrictCard import DistrictCard
from Player import Player

characterOrder = {0: 'Assasin',
                  1: 'Thief',
                  2: 'Magician',
                  3: 'King',
                  4: 'Bishop',
                  5: 'Merchant',
                  6: 'Architect',
                  7: 'Warlord'
                  }



class Logic:
    def __init__(self):
        self.round = 0
        self.step = 0
        self.turn = 0

        self.action = 0
        self.skill = 0

        self.player: List[Player] = []
        self.cc: List[CharacterCard] = []
        self.ccIngame: List[CharacterCard] = []
        self.dc: List[DistrictCard] = []
        self.gold = 0

        self.listener = {}

    def addPlayer(self, player: Player):
        for x in self.player:
            if x == player:
                raise Exception('player already added')
        self.player.append(player)

    def startGame(self):
        self.call('<<events>>', event='GameStart')
        self.round = 1
        self.step = 2
        self.call('<<events>>', event='NextPlayer', player=self._getCurrentPlayer())

    def chooseCharacterCard(self, player: Player, cc: CharacterCard):
        self._checkOption('chooseCharacter')
        self._checkPlayer(player)
        self.ccIngame.remove(cc)

    def pickGold(self, player: Player):
        self._checkPlayer(player)
        if self.action >= 1:
            raise Exception('already done')
        self.action += 1
        self.gold -= 2
        player.coins += 2

    def pickDistrictCard(self, player: Player):
        self._checkPlayer(player)
        if self.action >= 1:
            raise Exception('already done')
        self.action += 1
        dc = self.dc.pop()
        player.hand.append(dc)

    def _checkPlayer(self, player: Player):
        if not self._isCurrentPlayer(player):
            raise Exception('not your turn')

    def _checkOption(self, option):
        if option is not self.getOptions():
            raise Exception('not an option')

    def _isCurrentPlayer(self, player: Player):
        if self.turn >= len(self.player):
            return False
        if self.step == 3:
            return self.ccIngame[self.turn] == player.cc
        else:
            return self.player[self.turn] == player

    def _getCurrentPlayer(self):
        if self.turn >= len(self.player):
            return None
        if self.step == 3:
            for x in self.player:
                if x.cc == self.ccIngame[self.turn]:
                    return x
            return None
        else:
            return self.player[self.turn]

    def useCharacterSkill(self, player: Player):
        self._checkPlayer(player)

    def buildDistrictCard(self, player: Player, dc: DistrictCard):
        self._checkPlayer(player)
        if dc not in player.hand:
            raise Exception('card not in hand')
        if dc.cost > player.coins:
            raise Exception('not enough gold')
        player.hand.remove(dc)
        player.dc.append(dc)

    def endTurn(self, player: Player):
        self._checkPlayer(player)
        self.turn += 1
        self.action = 0
        self.skill = 0
        self.call('<<events>>', event='NextPlayer', player=self._getCurrentPlayer())
        pass

    def bind(self, eventName: str, callable):
        l = self.listener.get(eventName)
        if l == None:
            l = []
            self.listener[eventName] = l
        l.append(callable)

    def call(self, eventName: str, *args, **kv):
        list = self.listener.get(eventName)
        if list != None:
            for x in list:
                x(*args, **kv)

    def getOptions(self):
        ret = []

        if self.step == 2:
            ret.append('chooseCharacter')
        elif self.step == 3:
            if self.skill == 0:
                ret.append('useSkill')
            if self.action == 0:
                ret.append('drawTwoGold')
                ret.append('drawTwoDistrictCards')
            elif self.action == 1:
                ret.append('buildDistrictCard')
                ret.append('endTurn')
            elif self.action == 2:
                ret.append('endTurn')

        return ret

    def getAvailableCharacters(self):
        return self.ccIngame


