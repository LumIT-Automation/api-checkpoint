from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.Rule import Rule

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetInfo
from checkpoint.controllers.CustomControllerPatch import CustomControllerCheckPointUpdate
from checkpoint.controllers.CustomControllerDelete import CustomControllerCheckPointDelete


class CheckPointRuleController(CustomControllerCheckPointGetInfo, CustomControllerCheckPointUpdate, CustomControllerCheckPointDelete):
    def __init__(self, ruleType: str, *args, **kwargs):
        CustomControllerCheckPointGetInfo.__init__(self, subject="rule", *args, **kwargs)

        self.ruleType = ruleType



    def get(self, request: Request, assetId: int, domain: str, layerUid: str, ruleUid: str) -> Response:
        return self.getInfo(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=ruleUid,
            objectType=self.ruleType,
            actionCallback=lambda: Rule(sessionId="", ruleType=self.ruleType, assetId=assetId, domain=domain, layerUid=layerUid, uid=ruleUid).info(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def delete(self, request: Request, assetId: int, domain: str, layerUid: str, ruleUid: str) -> Response:
        return self.remove(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=ruleUid,
            objectType=self.ruleType,
            actionCallback=lambda: Rule(sessionId=self.sessionId, ruleType=self.ruleType, assetId=assetId, domain=domain, layerUid=layerUid, uid=ruleUid).delete(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def patch(self, request: Request, assetId: int, domain: str, layerUid: str, ruleUid: str) -> Response:
        def actionCallback(data):
            Rule(sessionId=self.sessionId, ruleType=self.ruleType, assetId=assetId, domain=domain, layerUid=layerUid, uid=ruleUid).modify(data)

        return self.modify(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=ruleUid,
            objectType=self.ruleType,
            actionCallback=actionCallback,
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
