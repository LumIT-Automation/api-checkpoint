from typing import List

from checkpoint.models.CheckPoint.Object import Object
from checkpoint.models.CheckPoint.backend.Host import Host as Backend

from checkpoint.helpers.Misc import Misc
from checkpoint.helpers.Log import Log


class Host(Object):
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



    def modify(self, data: dict, autoPublish: bool = True) -> None:
        try:
            Backend.modify(self.sessionId, self.assetId, self.domain, self.uid, data, autoPublish)

            for k, v in Misc.toDict(data).items():
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
    def listQuick(sessionId: str, assetId: int, domain: str, localOnly: bool = False, filter: str = "") -> List[dict]:
        out = list()

        try:
            if localOnly and domain != "Global":
                o = Backend.list(sessionId, assetId, domain, filter=filter)
                for el in o:
                    if "domain" in el and "domain-type" in el["domain"]:
                        if el["domain"]["domain-type"] != "global domain":
                            out.append(el)
            else:
                out = Backend.list(sessionId, assetId, domain, filter=filter)

            return out
        except Exception as e:
            raise e



    @staticmethod
    def searchByIpv4Addresses(sessionId: str, assetId: int, domain: str, ipv4: str, localOnly: bool = False) -> List[dict]:
        out = list()

        try:
            l = Host.listQuick(sessionId, assetId, domain, localOnly=localOnly, filter=ipv4) # oh gosh, no exact match available.
            for el in l:
                if "ipv4-address" in el:
                    if el["ipv4-address"] == ipv4:
                        out.append(el) # more than one IPv4 address can coexist (with different names).
        except Exception as e:
            raise e

        return out



    @staticmethod
    def add(sessionId: str, assetId: int, domain: str, data: dict, autoPublish: bool = True) -> dict:
        out = dict()

        try:
            o = Backend.add(sessionId, assetId, domain, data, autoPublish)
            out["uid"] = o.get("uid", "")
        except Exception as e:
            raise e

        return out
