from typing import List

from django.conf import settings

from checkpoint.models.CheckPoint.Session import Session

from checkpoint.helpers.ApiSupplicant import ApiSupplicant
from checkpoint.helpers.Log import Log

class Layer:
    def __init__(self, sessionId: str, layerType: str, assetId: int, domain: str, uid: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = sessionId
        if layerType not in ("access", "threat", "https"):
            raise NotImplementedError

        self.type: str = layerType
        self.assetId: int = int(assetId)
        self.domain: str = domain
        self.uid: str = uid



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self) -> dict:
        try:
            return ApiSupplicant(self.sessionId, self.assetId).post(
                urlSegment="show-"+self.type+"-layer",
                domain=self.domain,
                data={
                    "uid": self.uid,
                    "details-level": "full"
                }
            )
        except Exception as e:
            raise e



    def modify(self, data: dict, autoPublish: bool = True) -> None:
        data["uid"] = self.uid

        try:
            ApiSupplicant(self.sessionId, self.assetId).post(
                urlSegment="set-"+self.type+"-layer",
                domain=self.domain,
                data=data
            )

            if autoPublish:
                Session(sessionId=self.sessionId, assetId=self.assetId, domain=self.domain).publish()
        except Exception as e:
            if autoPublish:
                Session(sessionId=self.sessionId, assetId=self.assetId, domain=self.domain).discard()

            raise e



    def delete(self, autoPublish: bool = True) -> None:
        try:
            ApiSupplicant(self.sessionId, self.assetId).post(
                urlSegment="delete-"+self.type+"-layer",
                domain=self.domain,
                data={
                    "uid": self.uid
                }
            )

            if autoPublish:
                Session(sessionId=self.sessionId, assetId=self.assetId, domain=self.domain).publish()
        except Exception as e:
            if autoPublish:
                Session(sessionId=self.sessionId, assetId=self.assetId, domain=self.domain).discard()

            raise e



    def list(self, details: str = "standard") -> List[dict]:
        out = list()
        limit = 500

        try:
            # Collect all data (serial requests).
            for n in range(0, settings.MAX_REQUESTS):
                o = ApiSupplicant(self.sessionId, self.assetId, silent=True).post(
                    urlSegment="show-"+self.type+"-layers",
                    domain=self.domain,
                    data={
                        "details-level": details,
                        "limit": limit,
                        "offset": limit * n
                    }
                )

                l = self.type+"-layers"
                if l in o and o[l]:
                    out.extend(o[l])
                    if o["to"] >= o["total"]:
                        break
                else:
                    break

            return out
        except Exception as e:
            raise e



    def add(self, data: dict, autoPublish: bool = True) -> dict:
        try:
            o = ApiSupplicant(self.sessionId, self.assetId).post(
                urlSegment="add-"+self.type+"-layer",
                domain=self.domain,
                data=data
            )

            if autoPublish:
                Session(sessionId=self.sessionId, assetId=self.assetId, domain=self.domain).publish()

            return o
        except Exception as e:
            if autoPublish:
                Session(sessionId=self.sessionId, assetId=self.assetId, domain=self.domain).discard()

            raise e



    def listRules(self) -> List[dict]:
        out = list()
        limit = 500

        try:
            # Collect all data (serial requests).
            for n in range(0, settings.MAX_REQUESTS):
                o = ApiSupplicant(self.sessionId, self.assetId).post(
                    urlSegment="show-"+self.type+"-rulebase",
                    domain=self.domain,
                    data={
                        "details-level": "standard",
                        "limit": limit,
                        "offset": limit * n,
                        "uid": self.uid # layer uid.
                    }
                )

                if "rulebase" in o and o["rulebase"]:
                    out.extend(o["rulebase"])
                    if o["to"] >= o["total"]:
                        break
                else:
                    break

            return out
        except Exception as e:
            raise e
