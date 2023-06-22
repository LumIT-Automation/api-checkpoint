from checkpoint.models.CheckPoint.Session import Session

from checkpoint.helpers.ApiSupplicant import ApiSupplicant


class Rule:
    def __init__(self, sessionId: str, ruleType: str, assetId: int, domain: str, layerUid: str = "", uid: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = sessionId
        if ruleType not in ("access", "threat", "https"):
            raise NotImplementedError

        self.type: str = ruleType
        self.assetId: int = int(assetId)
        self.domain: str = domain
        self.layerUid: str = layerUid
        self.uid: str = uid



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self) -> dict:
        try:
            return ApiSupplicant(self.sessionId, self.assetId).post(
                urlSegment="show-" + self.type + "-rule",
                domain=self.domain,
                data={
                    "uid": self.uid,
                    "details-level": "full",
                    "layer": self.layerUid
                }
            )
        except Exception as e:
            raise e



    def modify(self, data: dict, autoPublish: bool = True) -> None:
        data.update({
            "uid": self.uid,
            "layer": self.layerUid
        })

        try:
            ApiSupplicant(self.sessionId, self.assetId).post(
                urlSegment="set-" + self.type + "-rule",
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
                urlSegment="delete-" + self.type + "-rule",
                domain=self.domain,
                data={
                    "uid": self.uid,
                    "layer": self.layerUid
                }
            )

            if autoPublish:
                Session(sessionId=self.sessionId, assetId=self.assetId, domain=self.domain).publish()
        except Exception as e:
            if autoPublish:
                Session(sessionId=self.sessionId, assetId=self.assetId, domain=self.domain).discard()

            raise e



    def add(self, data: dict, autoPublish: bool = True) -> dict:
        data.update({
            "layer": self.layerUid
        })

        try:
            o = ApiSupplicant(self.sessionId, self.assetId).post(
                urlSegment="add-" + self.type + "-rule",
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
