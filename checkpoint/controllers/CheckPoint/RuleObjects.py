from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.RuleObject import RuleObject

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetList
from checkpoint.controllers.CustomControllerPost import CustomControllerCheckPointCreate


class RuleObjectsControllerFactory:
    def __init__(self, ruleType):
        self.ruleType = ruleType

    def __call__(self, *args, **kwargs):
        try:
            if self.ruleType == "access":
                from checkpoint.serializers.CheckPoint.RuleObjectsAccess import CheckPointRuleObjectsAccessSerializer as Serializer
            elif self.ruleType == "https":
                from checkpoint.serializers.CheckPoint.RuleObjectsHttps import CheckPointRuleObjectsHttpsSerializer as Serializer
            elif self.ruleType == "threat":
                from checkpoint.serializers.CheckPoint.RuleObjectsThreat import CheckPointRuleObjectsThreatSerializer as Serializer
            else:
                raise NotImplementedError

            return Serializer
        except Exception as e:
            raise e



class CheckPointRuleObjectsController(CustomControllerCheckPointGetList, CustomControllerCheckPointCreate):
    def __init__(self, ruleType: str, *args, **kwargs):
        super().__init__(subject="rule_object", *args, **kwargs)

        self.ruleType = ruleType



    def get(self, request: Request, assetId: int, domain: str, layerUid: str, ruleUid: str) -> Response:
        return self.getList(
            request=request,
            assetId=assetId,
            domain=domain,
            objectType=self.ruleType,
            actionCallback=lambda: RuleObject.listObjectsInRule(sessionId="", ruleType=self.ruleType, assetId=assetId, domain=domain, layerUid=layerUid, ruleUid=ruleUid),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def post(self, request: Request, assetId: int, domain: str, layerUid: str, ruleUid: str) -> Response:
        return self.create(
            request=request,
            assetId=assetId,
            domain=domain,
            objectType=self.ruleType,
            Serializer=RuleObjectsControllerFactory(self.ruleType)(), # get suitable Serializer.
            actionCallback=lambda data: RuleObject.addObjectsToRule(sessionId=self.sessionId, ruleType=self.ruleType, assetId=assetId, domain=domain, layerUid=layerUid, ruleUid=ruleUid, data=data),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
