from checkpoint.models.CheckPoint.NatRule import NatRule


class NatRuleObject:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def listObjectsInNatRule(sessionId: str, assetId: int, domain: str, packageUid: str, natRuleUid: str) -> dict:
        o = dict()

        try:
            info = NatRule(sessionId=sessionId, assetId=assetId, domain=domain, packageUid=packageUid, uid=natRuleUid).info()
            for t in ("original-destination", "translated-destination", "original-source", "translated-source"):
                o[t] = {}

                try:
                    o[t] = info[t]["uid"]
                except Exception:
                    pass

        except Exception as e:
            raise e

        return o



    @staticmethod
    def addObjectsToNatRule(sessionId: str, assetId: int, domain: str, packageUid: str, natRuleUid: str, data: dict) -> None:
        try:
            for t in ("original-destination", "translated-destination", "original-source", "translated-source"):
                if t in data and data[t]:
                    NatRule(sessionId=sessionId, assetId=assetId, domain=domain, packageUid=packageUid, uid=natRuleUid).modify({
                        t: data[t]
                    })
        except Exception as e:
            raise e
