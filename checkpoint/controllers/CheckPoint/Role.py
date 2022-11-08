from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.Role import Role

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetInfo


class CheckPointRoleController(CustomControllerCheckPointGetInfo):
    def __init__(self, *args, **kwargs):
        CustomControllerCheckPointGetInfo.__init__(self, subject="role", *args, **kwargs)


    def get(self, request: Request, assetId: int, domain: str, roleUid: str) -> Response:
        return self.getInfo(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=roleUid,
            actionCallback=lambda: Role(sessionId="", assetId=assetId, domain=domain, uid=roleUid).info(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
