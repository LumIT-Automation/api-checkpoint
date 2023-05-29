from datetime import datetime
from random import randrange


class Misc:
    @staticmethod
    def getWorkflowCorrelationId() -> str:
        return str(datetime.now().strftime("%Y%m%d:%H%M-")) + str(randrange(0, 9999))



    @staticmethod
    def deepRepr(o) -> dict:
        try:
            r = dict()

            try:
                v = vars(o)
            except TypeError:
                v = o

            if isinstance(v, dict):
                for key, val in v.items():
                    if isinstance(val, str) or isinstance(val, int) or isinstance(val, bool) or not val:
                        r[key] = val

                    elif isinstance(val, list):
                        for j in val:
                            if key not in r:
                                r[key] = list()
                            r[key].append(Misc.deepRepr(j))

                    else:
                        if key not in r:
                            r[key] = dict()
                        r[key] = Misc.deepRepr(val)
        except Exception as e:
            raise e

        return r
