from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.Group import Group
from checkpoint.models.Permission.Permission import Permission

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetList


class CheckPointGroupFatherGroupsController(CustomControllerCheckPointGetList):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="group", *args, **kwargs)



    def get(self, request: Request, assetId: int, domain: str, groupUid: str) -> Response:
        return self.getList(
            request=request,
            assetId=assetId,
            domain=domain,
            containerObjectUid=groupUid,
            actionCallback=lambda: Group(sessionId="", assetId=assetId, domain=domain, uid=groupUid).listFatherGroups(),
            permission={
                "method": Permission.hasUserPermission,
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
