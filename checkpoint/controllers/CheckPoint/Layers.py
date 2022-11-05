from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.Layer import Layer
from checkpoint.models.Permission.Permission import Permission

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetList
from checkpoint.controllers.CustomControllerPost import CustomControllerCheckPointCreate


class LayerControllerFactory:
    def __init__(self, layerType):
        self.layerType = layerType

    def __call__(self, *args, **kwargs):
        try:
            if self.layerType == "access":
                from checkpoint.serializers.CheckPoint.LayerAccess import CheckPointLayerAccessSerializer as Serializer
            elif self.layerType == "threat":
                from checkpoint.serializers.CheckPoint.LayerThreat import CheckPointLayerThreatSerializer as Serializer
            elif self.layerType == "https":
                from checkpoint.serializers.CheckPoint.LayerHttps import CheckPointLayerHttpsSerializer as Serializer

            else:
                raise NotImplementedError

            return Serializer
        except Exception as e:
            raise e



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
                "method": Permission.hasUserPermission,
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
            Serializer=LayerControllerFactory(self.layerType)(), # get suitable Serializer.
            actionCallback=lambda data: Layer.add(sessionId=self.sessionId, layerType=self.layerType, assetId=assetId, domain=domain, data=data),
            permission={
                "method": Permission.hasUserPermission,
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
