from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.Permission.Permission import Permission

from checkpoint.serializers.Permission.Permission import PermissionSerializer as PermissionSerializer
from checkpoint.serializers.Permission.Permissions import PermissionsSerializer as PermissionsSerializer

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetList
from checkpoint.controllers.CustomControllerPost import CustomControllerCheckPointCreate


class PermissionsController(CustomControllerCheckPointGetList, CustomControllerCheckPointCreate):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="permission_identityGroup", *args, **kwargs)



    def get(self, request: Request) -> Response:
        return self.getList(
            request=request,
            Serializer=PermissionsSerializer,
            actionCallback=lambda: Permission.permissionsDataList(),
            permission={
                "args": {
                }
            }
        )



    def post(self, request: Request) -> Response:
        def actionCallback(data):
            return Permission.addFacade(
                identityGroupIdentifier=data["identity_group_identifier"],
                role=data["role"],
                domainInfo={
                    "assetId": data["domain"]["id_asset"],
                    "name": data["domain"]["name"]
                }
            )

        return self.create(
            request=request,
            Serializer=PermissionSerializer,
            actionCallback=lambda data: actionCallback(data),
            permission={
                "args": {
                }
            }
        )
