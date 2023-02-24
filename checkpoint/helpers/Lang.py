import re
import collections


class Lang:
    @staticmethod
    def stripQuotes(sentence: str) -> str:
        # Unquotes sentence.
        if sentence:
            sentence = sentence.strip()
            if re.search("^[\'\"].*[\'\"]$", sentence):
                sentence = sentence[1:-1]

        return sentence



    @staticmethod
    def toDict(layer):
        r = layer
        if isinstance(layer, collections.OrderedDict):
            r = dict(layer)

        try:
            for key, value in r.items():
                r[key] = Lang.toDict(value)
        except AttributeError:
            pass

        return r
