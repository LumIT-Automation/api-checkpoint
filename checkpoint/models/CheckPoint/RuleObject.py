from checkpoint.models.CheckPoint.Rule import Rule


class RuleObject:
    def __init__(self, sessionId: str, ruleType: str, assetId: int, domain: str, layerUid: str, ruleUid: str, objectUid: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = sessionId
        self.ruleType: str = ruleType
        self.assetId: int = int(assetId)
        self.domain: str = domain
        self.layer: str = layerUid
        self.rule: str = ruleUid
        self.object: str = objectUid



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def remove(self, autoPublish: bool = True) -> None:
        try:
            # Remove both in source and destination.
            # Removal will fail for the last rule, with a 400 as a return HTTP code.
            Rule(sessionId=self.sessionId, ruleType=self.ruleType, assetId=self.assetId, domain=self.domain, layerUid=self.layer, uid=self.rule).modify(
                {
                    "source": {
                        "remove": self.object
                    },
                    "destination": {
                        "remove": self.object
                    }
                },
                autoPublish=autoPublish)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def listObjectsInRule(sessionId: str, ruleType: str, assetId: int, domain: str, layerUid: str, ruleUid: str) -> dict:
        o = {
            "source": list(),
            "destination": list(),
        }

        try:
            info = Rule(sessionId=sessionId, ruleType=ruleType, assetId=assetId, domain=domain, layerUid=layerUid, uid=ruleUid).info()
            for t in ("source", "destination"):
                try:
                    for el in info[t]:
                        if "uid" in el:
                            o[t].append(el["uid"])
                except Exception:
                    pass

        except Exception as e:
            raise e

        return o



    @staticmethod
    def addObjectsToRule(sessionId: str, ruleType: str, assetId: int, domain: str, layerUid: str, ruleUid: str, data: dict, autoPublish: bool = True) -> None:
        try:
            for t in ("source", "destination"):
                if t not in data:
                    data[t] = list()

            # Put hosts.
            Rule(sessionId=sessionId, ruleType=ruleType, assetId=assetId, domain=domain, layerUid=layerUid, uid=ruleUid).modify(
                {
                    "source": {
                        "add": data["source"]
                    },
                    "destination": {
                        "add": data["destination"]
                    }
                },
                autoPublish=autoPublish)
        except Exception as e:
            raise e
