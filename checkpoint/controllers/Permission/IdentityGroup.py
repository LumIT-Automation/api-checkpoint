from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.Permission.IdentityGroup import IdentityGroup
from checkpoint.models.Permission.Permission import Permission

from checkpoint.serializers.Permission.IdentityGroup import IdentityGroupSerializer as GroupSerializer

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetInfo
from checkpoint.controllers.CustomControllerPatch import CustomControllerCheckPointUpdate
from checkpoint.controllers.CustomControllerDelete import CustomControllerCheckPointDelete


class PermissionIdentityGroupController(CustomControllerCheckPointGetInfo, CustomControllerCheckPointUpdate, CustomControllerCheckPointDelete):
    def __init__(self, *args, **kwargs):
        CustomControllerCheckPointGetInfo.__init__(self, subject="permission_identityGroup", *args, **kwargs)



    def delete(self, request: Request, identityGroupIdentifier: str) -> Response:
        return self.remove(
            request=request,
            obj={
                "uid": identityGroupIdentifier
            },
            actionCallback=lambda: IdentityGroup(identityGroupIdentifier=identityGroupIdentifier).delete(),
            permission={
                "method": Permission.hasUserPermission,
                "args": {
                }
            }
        )



    def patch(self, request: Request, identityGroupIdentifier: str) -> Response:
        return self.modify(
            request=request,
            objectUid=identityGroupIdentifier,
            Serializer=GroupSerializer,
            actionCallback=lambda data: IdentityGroup(identityGroupIdentifier=identityGroupIdentifier).modify(data),
            permission={
                "method": Permission.hasUserPermission,
                "args": {
                }
            }
        )
