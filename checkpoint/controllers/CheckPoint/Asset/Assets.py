from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.Asset.Asset import Asset
from checkpoint.models.Permission.Permission import Permission

from checkpoint.serializers.CheckPoint.Asset.Asset import CheckPointAssetSerializer as AssetSerializer
from checkpoint.serializers.CheckPoint.Asset.Assets import CheckPointAssetsSerializer as AssetsSerializer

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetList
from checkpoint.controllers.CustomControllerPost import CustomControllerCheckPointCreate


class CheckPointAssetsController(CustomControllerCheckPointGetList, CustomControllerCheckPointCreate):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="asset", *args, **kwargs)



    def get(self, request: Request) -> Response:
        return self.getList(
            request=request,
            Serializer=AssetsSerializer,
            actionCallback=lambda: Asset.list(),
            permission={
                "method": Permission.hasUserPermission,
                "args": {
                }
            }
        )



    def post(self, request: Request) -> Response:
        return self.create(
            request=request,
            Serializer=AssetSerializer,
            actionCallback=lambda data: Asset.add(data),
            permission={
                "method": Permission.hasUserPermission,
                "args": {
                }
            }
        )
