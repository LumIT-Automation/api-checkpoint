from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.Asset.Asset import Asset

from checkpoint.serializers.CheckPoint.Asset.Asset import CheckPointAssetSerializer as Serializer

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetInfo
from checkpoint.controllers.CustomControllerPatch import CustomControllerCheckPointUpdate
from checkpoint.controllers.CustomControllerDelete import CustomControllerCheckPointDelete


class CheckPointAssetController(CustomControllerCheckPointGetInfo, CustomControllerCheckPointUpdate, CustomControllerCheckPointDelete):
    def __init__(self, *args, **kwargs):
        CustomControllerCheckPointGetInfo.__init__(self, subject="asset", *args, **kwargs)



    def delete(self, request: Request, assetId: int) -> Response:
        return self.remove(
            request=request,
            assetId=0,
            objectUid=str(assetId),
            actionCallback=lambda: Asset(assetId).delete(),
            permission={
                "args": {
                    "assetId": assetId
                }
            }
        )



    def patch(self, request: Request, assetId: int) -> Response:
        return self.modify(
            request=request,
            assetId=0,
            objectUid=str(assetId),
            Serializer=Serializer,
            actionCallback=lambda data: Asset(assetId).modify(data),
            permission={
                "args": {
                    "assetId": assetId
                }
            }
        )
