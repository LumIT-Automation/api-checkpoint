from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.Layer import Layer
from checkpoint.models.Permission.Permission import Permission

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetInfo
from checkpoint.controllers.CustomControllerPatch import CustomControllerCheckPointUpdate
from checkpoint.controllers.CustomControllerDelete import CustomControllerCheckPointDelete


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



class CheckPointLayerController(CustomControllerCheckPointGetInfo, CustomControllerCheckPointUpdate, CustomControllerCheckPointDelete):
    def __init__(self, layerType: str, *args, **kwargs):
        CustomControllerCheckPointGetInfo.__init__(self, subject="layer", *args, **kwargs)

        self.layerType = layerType



    def get(self, request: Request, assetId: int, domain: str, layerUid: str) -> Response:
        return self.getInfo(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=layerUid,
            objectType=self.layerType,
            actionCallback=lambda: Layer(sessionId="", layerType=self.layerType, assetId=assetId, domain=domain, uid=layerUid).info(),
            permission={
                "method": Permission.hasUserPermission,
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def delete(self, request: Request, assetId: int, domain: str, layerUid: str) -> Response:
        return self.remove(
            request=request,
            assetId=assetId,
            domain=domain,
            obj={
                "uid": layerUid,
                "class": self.layerType
            },
            actionCallback=lambda: Layer(sessionId=self.sessionId, layerType=self.layerType, assetId=assetId, domain=domain, uid=layerUid).delete(),
            permission={
                "method": Permission.hasUserPermission,
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def patch(self, request: Request, assetId: int, domain: str, layerUid: str) -> Response:
        return self.modify(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=layerUid,
            objectType=self.layerType,
            Serializer=LayerControllerFactory(self.layerType)(), # get suitable Serializer.
            actionCallback=lambda data: Layer(sessionId=self.sessionId, layerType=self.layerType, assetId=assetId, domain=domain, uid=layerUid).modify(data),
            permission={
                "method": Permission.hasUserPermission,
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
