from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.NatRule import NatRule

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetInfo
from checkpoint.controllers.CustomControllerDelete import CustomControllerCheckPointDelete


class CheckPointNatRuleController(CustomControllerCheckPointGetInfo, CustomControllerCheckPointDelete):
    def __init__(self, *args, **kwargs):
        CustomControllerCheckPointGetInfo.__init__(self, subject="nat_rule", *args, **kwargs)


    def get(self, request: Request, assetId: int, domain: str, packageUid: str, natRuleUid: str) -> Response:
        return self.getInfo(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=natRuleUid,
            actionCallback=lambda: NatRule(sessionId="", assetId=assetId, domain=domain, packageUid=packageUid, uid=natRuleUid).info(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def delete(self, request: Request, assetId: int, domain: str, packageUid: str, natRuleUid: str) -> Response:
        return self.remove(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=natRuleUid,
            actionCallback=lambda: NatRule(sessionId=self.sessionId, assetId=assetId, domain=domain, packageUid=packageUid, uid=natRuleUid).delete(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
