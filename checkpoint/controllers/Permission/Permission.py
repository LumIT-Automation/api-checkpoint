from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.Permission.IdentityGroup import IdentityGroup
from checkpoint.models.Permission.Role import Role
from checkpoint.models.Permission.Domain import Domain
from checkpoint.models.Permission.Permission import Permission

from checkpoint.serializers.Permission.Permission import PermissionSerializer as Serializer

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetInfo
from checkpoint.controllers.CustomControllerPatch import CustomControllerCheckPointUpdate
from checkpoint.controllers.CustomControllerDelete import CustomControllerCheckPointDelete

from checkpoint.helpers.Exception import CustomException


class PermissionController(CustomControllerCheckPointGetInfo, CustomControllerCheckPointUpdate, CustomControllerCheckPointDelete):
    def __init__(self, *args, **kwargs):
        CustomControllerCheckPointGetInfo.__init__(self, subject="permission_identityGroup", *args, **kwargs)



    def delete(self, request: Request, permissionId: int) -> Response:
        return self.remove(
            request=request,
            obj={
                "uid": str(permissionId)
            },
            actionCallback=lambda: Permission(permissionId).delete(),
            permission={
                "method": Permission.hasUserPermission,
                "args": {
                }
            }
        )



    def patch(self, request: Request, permissionId: int) -> Response:
        def actionCallback(data):
            return Permission.modifyFacade(
                permissionId=permissionId,
                identityGroupId=data["identity_group_identifier"],
                role=data["role"],
                domainInfo={
                    "assetId": data["domain"]["id_asset"],
                    "name": data["domain"]["name"]
                }
            )

        return self.modify(
            request=request,
            objectUid=str(permissionId),
            Serializer=Serializer,
            actionCallback=lambda data: actionCallback(data),
            permission={
                "method": Permission.hasUserPermission,
                "args": {
                }
            }
        )
