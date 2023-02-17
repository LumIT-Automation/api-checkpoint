import collections
from datetime import datetime
from random import randrange


class Misc:
    @staticmethod
    def getWorkflowCorrelationId() -> str:
        return str(datetime.now().strftime("%Y%m%d:%H%M-")) + str(randrange(0, 9999))



    @staticmethod
    def toDict(layer):
        r = layer
        if isinstance(layer, collections.OrderedDict):
            r = dict(layer)

        try:
            for key, value in r.items():
                r[key] = Misc.toDict(value)
        except AttributeError:
            pass

        return r
