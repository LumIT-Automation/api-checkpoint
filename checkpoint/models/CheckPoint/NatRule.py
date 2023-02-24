from checkpoint.models.CheckPoint.backend.NatRule import NatRule as Backend

from checkpoint.helpers.Lang import Lang


class NatRule:
    def __init__(self, sessionId: str, assetId: int, domain: str, packageUid: str, uid: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = sessionId
        self.assetId: int = int(assetId)
        self.domain: str = domain
        self.packageUid: str = packageUid
        self.uid: str = uid



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self) -> dict:
        try:
            return Backend.info(self.sessionId, self.assetId, self.domain, self.packageUid, self.uid)
        except Exception as e:
            raise e



    def modify(self, data: dict, autoPublish: bool = True) -> None:
        try:
            Backend.modify(self.sessionId, self.assetId, self.domain, self.packageUid, self.uid, data, autoPublish)

            for k, v in Lang.toDict(data).items():
                setattr(self, k, v)
        except Exception as e:
            raise e



    def delete(self, autoPublish: bool = True) -> None:
        try:
            Backend.delete(self.sessionId, self.assetId, self.domain, self.packageUid, self.uid, autoPublish)
            del self
        except Exception as e:
            raise e
