from typing import List

from checkpoint.models.CheckPoint.Object import Object
from checkpoint.models.CheckPoint.backend.Network import Network as Backend


class Network(Object):
    def __init__(self, sessionId: str, assetId: int, domain: str = "", name: str = "", uid: str = "", subnet4: str = "", *args, **kwargs):
        super().__init__(sessionId, assetId, domain, uid, *args, **kwargs)

        self.sessionId = sessionId
        self.assetId: int = int(assetId)
        self.domain: str = domain
        self.name: str = name
        self.uid: str = uid
        self.subnet4: str = subnet4



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
        except Exception as e:
            raise e
 


    def delete(self, autoPublish: bool = True) -> None:
        try:
            Backend.delete(self.sessionId, self.assetId, self.domain, self.uid, autoPublish)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def listQuick(sessionId: str, assetId: int, domain: str, localOnly: bool = False) -> List[dict]:
        try:
            out = list()

            if localOnly and domain != "Global":
                o = Backend.list(sessionId, assetId, domain)
                for el in o:
                    if "domain" in el and "domain-type" in el["domain"]:
                        if el["domain"]["domain-type"] != "global domain":
                            out.append(el)
            else:
                out = Backend.list(sessionId, assetId, domain)

            return out
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
