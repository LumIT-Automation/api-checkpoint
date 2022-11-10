from typing import List

from checkpoint.models.CheckPoint.Object import Object
from checkpoint.models.CheckPoint.backend.Task import Task as Backend


class Task(Object):
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
