from typing import List

from checkpoint.models.CheckPoint.backend.ApplicationSiteCategory import ApplicationSiteCategory as Backend

from checkpoint.helpers.Lang import Lang


class ApplicationSiteCategory:
    def __init__(self, sessionId: str, assetId: int, domain: str = "", name: str = "", uid: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = sessionId
        self.assetId: int = int(assetId)
        self.domain: str = domain
        self.name: str = name
        self.uid: str = uid



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self) -> dict:
        try:
            return Backend.info(self.sessionId, self.assetId, self.domain, self.uid)
        except Exception as e:
            raise e



    def modify(self, data: dict, autoPublish: bool = True) -> None:
        try:
            Backend.modify(self.sessionId, self.assetId, self.domain, self.uid, data, autoPublish)

            for k, v in Lang.toDict(data).items():
                setattr(self, k, v)
        except Exception as e:
            raise e



    def delete(self, autoPublish: bool = True) -> None:
        try:
            Backend.delete(self.sessionId, self.assetId, self.domain, self.uid, autoPublish)
            del self
        except Exception as e:
            raise e


    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def listQuick(sessionId: str, assetId: int, domain: str) -> List[dict]:
        try:
            return Backend.list(sessionId, assetId, domain)
        except Exception as e:
            raise e



    @staticmethod
    def add(sessionId: str, assetId: int, domain: str, data: dict, autoPublish: bool = True) -> dict:
        out = dict()

        try:
            o = Backend.add(sessionId, assetId, domain, data, autoPublish)
            out["uid"] = o.get("uid", "")
        except Exception as e:
            raise e

        return out
