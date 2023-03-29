from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.Ips import Ips

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetInfo


class CheckPointIpsController(CustomControllerCheckPointGetInfo):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="ips", *args, **kwargs)



    def get(self, request: Request, assetId: int, domain: str) -> Response:
        return self.getInfo(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid="status",
            actionCallback=lambda: Ips(sessionId="", assetId=assetId, domain=domain).info(),
            permission={
                "args": {
                    "assetId": assetId
                }
            }
        )
