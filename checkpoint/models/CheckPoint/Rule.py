class RuleBackendFactory:
    def __init__(self, ruleType):
        self.ruleType = ruleType

    def __call__(self, *args, **kwargs):
        try:
            if self.ruleType == "access":
                from checkpoint.models.CheckPoint.backend.RuleAccess import AccessRule as Backend
            elif self.ruleType == "threat":
                from checkpoint.models.CheckPoint.backend.RuleThreat import ThreatRule as Backend
            elif self.ruleType == "https":
                from checkpoint.models.CheckPoint.backend.RuleHttps import HttpsRule as Backend
            else:
                raise NotImplementedError

            return Backend
        except Exception as e:
            raise e



class Rule:
    def __init__(self, sessionId: str, ruleType: str, assetId: int, domain: str = "", name: str = "", layerUid: str = "", uid: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = sessionId
        self.type = ruleType
        self.assetId: int = int(assetId)
        self.domain: str = domain
        self.name: str = name
        self.layerUid: str = layerUid
        self.uid: str = uid

        self.Backend = RuleBackendFactory(ruleType)() # get suitable Backend.



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self) -> dict:
        try:
            return self.Backend(self.sessionId, self.assetId, self.domain, self.layerUid, self.uid).info()
        except Exception as e:
            raise e



    def modify(self, data: dict, autoPublish: bool = True) -> None:
        try:
            self.Backend(self.sessionId, self.assetId, self.domain, self.layerUid, self.uid).modify(data, autoPublish)
        except Exception as e:
            raise e
 


    def delete(self, autoPublish: bool = True) -> None:
        try:
            self.Backend(self.sessionId, self.assetId, self.domain, self.layerUid, self.uid).delete(autoPublish)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def add(sessionId: str, ruleType: str, assetId: int, domain: str, layerUid: str, data: dict, autoPublish: bool = True) -> dict:
        try:
            Backend = RuleBackendFactory(ruleType)() # get suitable Backend.
            return Backend(sessionId=sessionId, assetId=assetId, domain=domain, layerUid=layerUid).add(data, autoPublish)
        except Exception as e:
            raise e
 