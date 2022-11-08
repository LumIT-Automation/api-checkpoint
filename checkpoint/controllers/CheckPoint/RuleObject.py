from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.RuleObject import RuleObject

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetInfo
from checkpoint.controllers.CustomControllerPatch import CustomControllerCheckPointUpdate
from checkpoint.controllers.CustomControllerDelete import CustomControllerCheckPointDelete


class CheckPointRuleObjectController(CustomControllerCheckPointGetInfo, CustomControllerCheckPointUpdate, CustomControllerCheckPointDelete):
    def __init__(self, ruleType: str, *args, **kwargs):
        CustomControllerCheckPointGetInfo.__init__(self, subject="rule_object", *args, **kwargs)

        self.ruleType = ruleType



    def delete(self, request: Request, assetId: int, domain: str, layerUid: str, ruleUid: str, ruleObjectUid: str) -> Response:
        return self.remove(
            request=request,
            assetId=assetId,
            domain=domain,
            obj={
                "uid": ruleObjectUid,
                "containerUid": ruleUid
            },
            actionCallback=lambda: RuleObject(sessionId=self.sessionId, ruleType=self.ruleType, assetId=assetId, domain=domain, layerUid=layerUid, ruleUid=ruleUid, objectUid=ruleObjectUid).remove(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
