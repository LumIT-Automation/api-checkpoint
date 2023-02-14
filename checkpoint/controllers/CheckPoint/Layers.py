from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.Layer import Layer

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetList
from checkpoint.controllers.CustomControllerPost import CustomControllerCheckPointCreate


class CheckPointLayersController(CustomControllerCheckPointGetList, CustomControllerCheckPointCreate):
    def __init__(self, layerType: str, *args, **kwargs):
        super().__init__(subject="layer", *args, **kwargs)

        self.layerType = layerType



    def get(self, request: Request, assetId: int, domain: str) -> Response:
        def actionCallback():
            localOnly = False
            if "local" in request.GET:
                localOnly = True

            return Layer.listQuick(sessionId="", layerType=self.layerType, assetId=assetId, domain=domain, localOnly=localOnly)

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



    def post(self, request: Request, assetId: int, domain: str) -> Response:
        return self.create(
            request=request,
            assetId=assetId,
            domain=domain,
            objectType=self.layerType,
            actionCallback=lambda data: Layer.add(sessionId=self.sessionId, layerType=self.layerType, assetId=assetId, domain=domain, data=data),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
