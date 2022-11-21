from checkpoint.models.CheckPoint.backend.Object import Object as Backend


class Object:
    def __init__(self, sessionId: str, assetId: int, domain: str, uid: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = sessionId
        self.assetId: int = int(assetId)
        self.domain: str = domain
        self.uid: str = uid



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def whereUsed(self, indirect: bool = False) -> dict:
        try:
            return Backend.whereUsed(self.sessionId, self.assetId, self.domain, self.uid, indirect=indirect)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def listUnused(sessionId: str, assetId: int, domain: str) -> list:
        try:
            return Backend.listUnused(sessionId, assetId, domain)
        except Exception as e:
            raise e
