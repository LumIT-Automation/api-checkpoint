from checkpoint.models.CheckPoint.Object import Object
from checkpoint.models.CheckPoint.backend.User import User as Backend


class User(Object):
    def __init__(self, sessionId: str, assetId: int, domain: str, uid: str, *args, **kwargs):
        super().__init__(sessionId, assetId, domain, uid, *args, **kwargs)

        self.sessionId = sessionId
        self.assetId: int = int(assetId)
        self.domain: str = domain
        self.uid: str = uid



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self) -> dict:
        try:
            return Backend.info(self.sessionId, self.assetId, self.domain, self.uid)
        except Exception as e:
            raise e
