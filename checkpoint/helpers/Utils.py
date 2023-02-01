class CheckString:
    @staticmethod
    def check(s: str, lenght: int, badCharsStringSet: str = " ',][}{\"/\\"):
        if isinstance(s, str):
            if len(s) <= lenght:
                if not 1 in [c in s for c in badCharsStringSet]:  # return 1 if there is at least one bad char in s.
                    return s
        raise ValueError('Checkstring: Invalid string')


    @staticmethod
    def allowedChars(s: str, lenght: int, goodCharsStringSet: str):
        if isinstance(s, str):
            if len(s) <= lenght:
                if not 0 in [c in goodCharsStringSet for c in s]: # return 0 if there is at least one not good char in s.
                    return s
        raise ValueError('Checkstring: Invalid string')

