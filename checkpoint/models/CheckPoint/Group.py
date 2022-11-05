from typing import List

from checkpoint.models.CheckPoint.Object import Object
from checkpoint.models.CheckPoint.backend.Group import Group as Backend


class Group(Object):
    def __init__(self, sessionId: str, assetId: int, domain: str = "", uid: str = "", *args, **kwargs):
        super().__init__(sessionId, assetId, domain, uid, *args, **kwargs)

        self.sessionId = sessionId
        self.assetId: int = int(assetId)
        self.domain: str = domain
        self.uid: str = uid



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self, detail: str = "full") -> dict:
        try:
            return Backend.info(self.sessionId, self.assetId, self.domain, self.uid, detail)
        except Exception as e:
            raise e



    def listInnerGroups(self) -> List[dict]:
        o = list()

        try:
            members = self.info(detail="standard").get("members", [])
            for el in members:
                try:
                    if el["type"] == "group":
                        o.append(el)
                except Exception:
                    pass
        except Exception as e:
            raise e

        return o



    def listFatherGroups(self) -> List[dict]:
        o = list()

        try:
            members = self.info(detail="full").get("groups", [])
            for el in members:
                try:
                    if el["type"] == "group":
                        o.append(el)
                except Exception:
                    pass
        except Exception as e:
            raise e

        return o



    def modify(self, data: dict, autoPublish: bool = True) -> None:
        try:
            Backend.modify(self.sessionId, self.assetId, self.domain, self.uid, data, autoPublish)
        except Exception as e:
            raise e



    def addInnerGroup(self, groupUids: list) -> None:
        try:
            self.modify(
                data={
                    "members": {
                        "add": groupUids
                    }
                }
            )
        except Exception as e:
            raise e
 


    def delete(self, autoPublish: bool = True) -> None:
        try:
            Backend.delete(self.sessionId, self.assetId, self.domain, self.uid, autoPublish)
        except Exception as e:
            raise e



    def deleteInnerGroup(self, groupUid: str, autoPublish: bool = True) -> None:
        try:
            self.modify(
                data={
                    "members": {
                        "remove": groupUid
                    }
                },
                autoPublish=autoPublish
            )
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def listQuick(sessionId: str, assetId: int, domain: str, localOnly: bool = False) -> List[dict]:
        try:
            out = list()

            if localOnly:
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
