from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.Layer import Layer
from checkpoint.models.CheckPoint.Rule import Rule

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetList
from checkpoint.controllers.CustomControllerPost import CustomControllerCheckPointCreate


class CheckPointRulebaseController(CustomControllerCheckPointGetList, CustomControllerCheckPointCreate):
    def __init__(self, layerType: str, *args, **kwargs):
        super().__init__(subject="rulebase", *args, **kwargs)

        self.layerType = layerType



    def get(self, request: Request, assetId: int, domain: str, layerUid: str) -> Response:
        def actionCallback():
            localOnly = False
            if "local" in request.GET:
                localOnly = True

            return Layer.listRules(sessionId="", layerType=self.layerType, assetId=assetId, domain=domain, accessLayerUid=layerUid, localOnly=localOnly)

        return self.getList(
            request=request,
            assetId=assetId,
            domain=domain,
            objectType=self.layerType,
            actionCallback=actionCallback,
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def post(self, request: Request, assetId: int, domain: str, layerUid: str) -> Response:
        def actionCallback(data):
            return Rule.add(sessionId=self.sessionId, ruleType=self.layerType, assetId=assetId, domain=domain, layerUid=layerUid, data=data)

        return self.create(
            request=request,
            assetId=assetId,
            domain=domain,
            objectType=self.layerType,
            actionCallback=actionCallback,
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
