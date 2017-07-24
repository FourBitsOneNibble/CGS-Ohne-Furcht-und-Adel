from typing import Mapping, List

from Cards.CharacterCards.CharacterCard import CharacterCard
from KI import KI
from Logic import Logic
from Player import Player


class GUI:
    def __init__(self):
        self.exit = False
        self.logic = Logic()
        self.logic.bind('<<events>>', self.events)
        self.options = []

        self.user = []
        self.me = Player()
        self.logic.addPlayer(self.me)

        self.oDescription = {
            'chooseCharacter': 'Choose a Character'
        }

        self.oMethods = {
            'chooseCharacter': self._chooseCharacter
        }

        self.cmdCommands = {
            'exit':self._exit,
            'start':self._start,
            'addKI':self._addKI
        }
    def events(self, *args, **kv):
        event = kv['event']
        if event == 'GameStart':
            self._eventGameStart()
        elif event == 'NextPlayer':
            pass
        else:
            raise Exception('unhandled event:'+ event)

    def cmd(self, line):
        args = line.split()
        arg = args[0]

        m = self.cmdCommands.get(arg)
        if m == None:
            d = {str(i):v for i, v in enumerate(self.logic.getOptions())}
            opt = d.get(line)
            if opt == None:
                print('unknown command')
            else:
                self.oMethods[opt](args)
        else:
            m(args)




    def _addKI(self, *args):
        self.user.append(KI(self.logic))

    def _exit(self, *args):
        self.exit = True

    def _start(self, *args):
        self.logic.startGame()

    def loop(self):
        while not self.exit:


            self.printOptions()
            line = input('>> ')
            #print(line)
            self.cmd(line)

    def printOptions(self):
        ##print(self.logic.getOptions())

        options = self.logic.getOptions()
        if len(options) > 0:
            print('Choose option:')
            for i, x in enumerate(options):
                print('[' + str(i) + ']: ' + self.oDescription[x])


    def printOptions_(self):
        if len(self.options) == 0:
            return
        map : Mapping = self.options[len(self.options) - 1]
        for k,v in map.items():
            print('[' + k + ']: ' + v)

    def _chooseCharacter(self, *args):
        char = self.chooseCharacter(self.logic.getAvailableCharacters())
        if char == None:
            print('no such character')
        else:
            self.logic.chooseCharacterCard(self.me, char)

    def chooseCharacter(self, chars :List[CharacterCard]):
        print('Choose a Character:')
        dic = {str(i):c for i, c in enumerate(chars)}
        return dic.get(input('>> '))

    def _eventGameStart(self):
        self.cmdCommands.pop('addKI')
        self.cmdCommands.pop('start')


if __name__ == '__main__':
    gui = GUI()
    gui.loop()
