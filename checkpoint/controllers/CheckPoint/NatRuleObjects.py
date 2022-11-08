from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.NatRuleObject import NatRuleObject

from checkpoint.serializers.CheckPoint.NatRule import CheckPointNatRuleSerializer as Serializer

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetList
from checkpoint.controllers.CustomControllerPost import CustomControllerCheckPointCreate


class CheckPointNatRuleObjectsController(CustomControllerCheckPointGetList, CustomControllerCheckPointCreate):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="rule_object", *args, **kwargs)



    def get(self, request: Request, assetId: int, domain: str, packageUid: str, natRuleUid: str) -> Response:
        return self.getList(
            request=request,
            assetId=assetId,
            domain=domain,
            actionCallback=lambda: NatRuleObject.listObjectsInNatRule(sessionId="", assetId=assetId, domain=domain, packageUid=packageUid, natRuleUid=natRuleUid),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def post(self, request: Request, assetId: int, domain: str, packageUid: str, natRuleUid: str) -> Response:
        return self.create(
            request=request,
            assetId=assetId,
            domain=domain,
            Serializer=Serializer,
            actionCallback=lambda data: NatRuleObject.addObjectsToNatRule(sessionId=self.sessionId, assetId=assetId, domain=domain, packageUid=packageUid, natRuleUid=natRuleUid, data=data),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
