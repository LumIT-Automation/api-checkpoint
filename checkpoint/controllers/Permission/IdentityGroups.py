from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.Permission.IdentityGroup import IdentityGroup

from checkpoint.serializers.Permission.IdentityGroup import IdentityGroupSerializer as GroupSerializer
from checkpoint.serializers.Permission.IdentityGroups import IdentityGroupsSerializer as GroupsSerializer

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetList
from checkpoint.controllers.CustomControllerPost import CustomControllerCheckPointCreate


class PermissionIdentityGroupsController(CustomControllerCheckPointGetList, CustomControllerCheckPointCreate):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="permission_identityGroup", *args, **kwargs)



    def get(self, request: Request) -> Response:
        def actionCallback():
            showPrivileges = False
            if "related" in request.GET:
                rList = request.GET.getlist('related')
                if "privileges" in rList:
                    showPrivileges = True

            return IdentityGroup.listWithPermissionsPrivileges(showPrivileges=showPrivileges)

        return self.getList(
            request=request,
            Serializer=GroupsSerializer,
            actionCallback=actionCallback,
            permission={
                "args": {
                }
            }
        )



    def post(self, request: Request) -> Response:
        return self.create(
            request=request,
            Serializer=GroupSerializer,
            actionCallback=lambda data: IdentityGroup.add(data),
            permission={
                "args": {
                }
            }
        )
