from Logic import Logic
from User import User


class KI(User):
    def __init__(self, logic: Logic):
        super().__init__(logic)

    def playerEvents(self, *args, **kv):
        event = kv['event']
        if event == '':
            pass
        elif event == '':
            pass
        else:
            raise Exception(event + 'unhandled event')
