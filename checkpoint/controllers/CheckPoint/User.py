from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.User import User

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetInfo


class CheckPointUserController(CustomControllerCheckPointGetInfo):
    def __init__(self, *args, **kwargs):
        CustomControllerCheckPointGetInfo.__init__(self, subject="user", *args, **kwargs)


    def get(self, request: Request, assetId: int, domain: str, userUid: str) -> Response:
        return self.getInfo(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=userUid,
            actionCallback=lambda: User(sessionId="", assetId=assetId, domain=domain, uid=userUid).info(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
