from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.Asset.Asset import Asset

from checkpoint.serializers.CheckPoint.Asset.Asset import CheckPointAssetSerializer as AssetSerializer
from checkpoint.serializers.CheckPoint.Asset.Assets import CheckPointAssetsSerializer as AssetsSerializer

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetList
from checkpoint.controllers.CustomControllerPost import CustomControllerCheckPointCreate


class CheckPointAssetsController(CustomControllerCheckPointGetList, CustomControllerCheckPointCreate):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="asset", *args, **kwargs)



    def get(self, request: Request) -> Response:
        def actionCallback():
            from checkpoint.models.Permission.Permission import Permission
            from checkpoint.controllers.CustomControllerBase import CustomControllerBase

            permittedAssets = []
            user = CustomControllerBase.loggedUser(request)
            assets = Asset.list(showPassword=False)

            # Filter each asset basing on actual permissions.
            for a in assets:
                if Permission.hasUserPermission(groups=user["groups"], action="assets_get", assetId=a["id"]) or user["authDisabled"]:
                    permittedAssets.append(a)

            return permittedAssets


        return self.getList(
            request=request,
            Serializer=AssetsSerializer,
            actionCallback=actionCallback,
            permission={
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
                "args": {
                }
            }
        )
