from typing import List

from django.conf import settings

from checkpoint.models.CheckPoint.Session import Session

from checkpoint.helpers.ApiSupplicant import ApiSupplicant


class Service:
    def __init__(self, sessionId: str, serviceType: str, assetId: int, domain: str, uid: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = sessionId
        if serviceType not in ("tcp", "udp"):
            raise NotImplementedError

        self.type: str = serviceType
        self.assetId: int = int(assetId)
        self.domain: str = domain
        self.uid: str = uid



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self) -> dict:
        try:
            return ApiSupplicant(self.sessionId, self.assetId).post(
                urlSegment="show-service-"+self.type,
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
                urlSegment="set-service-"+self.type,
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
                urlSegment="delete-service-"+self.type,
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
                    urlSegment="show-services-"+self.type,
                    domain=self.domain,
                    data={
                        "details-level": details,
                        "limit": limit,
                        "offset": limit * n
                    }
                )

                if "objects" in o and o["objects"]:
                    out.extend(o["objects"])
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
                urlSegment="add-service-"+self.type,
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
