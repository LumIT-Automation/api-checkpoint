from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.Domain import Domain
from checkpoint.models.Permission.Permission import Permission

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetInfo


class CheckPointDomainController(CustomControllerCheckPointGetInfo):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="domain", *args, **kwargs)



    def get(self, request: Request, assetId: int, domainUid: str) -> Response:
        return self.getInfo(
            request=request,
            assetId=assetId,
            objectUid=domainUid,
            actionCallback=lambda: Domain(sessionId="", assetId=assetId, uid=domainUid).info(),
            permission={
                "method": Permission.hasUserPermission,
                "args": {
                    "assetId": assetId
                }
            }
        )
