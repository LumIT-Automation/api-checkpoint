from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.Permission.Role import Role

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetList

from checkpoint.serializers.Permission.Roles import RolesSerializer as Serializer


class PermissionRolesController(CustomControllerCheckPointGetList):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="permission_role", *args, **kwargs)



    def get(self, request: Request) -> Response:
        def actionCallback():
            loadPrivilege = False
            if "related" in request.GET:
                rList = request.GET.getlist('related')
                if "privileges" in rList:
                    loadPrivilege = True

            return [
                r.repr() for r in Role.list(loadPrivilege=loadPrivilege)
            ]

        return self.getList(
            request=request,
            Serializer=Serializer,
            actionCallback=actionCallback,
            permission={
                "args": {
                }
            }
        )
