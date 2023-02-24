class Network:
    @staticmethod
    def ipv4InRange(address: str, start: str, end: str) -> bool:
        def toTuple(i: str):
            return tuple(int(n) for n in i.split('.'))

        return toTuple(start) <= toTuple(address) <= toTuple(end)
