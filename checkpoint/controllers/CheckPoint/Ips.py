from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.Ips import Ips

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetInfo
from checkpoint.controllers.CustomControllerPut import CustomControllerCheckPointUpdateAll


class CheckPointIpsController(CustomControllerCheckPointGetInfo, CustomControllerCheckPointUpdateAll):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="ips", *args, **kwargs)

    def get(self, request: Request, assetId: int) -> Response:
        return self.getInfo(
            request=request,
            assetId=assetId,
            actionCallback=lambda: Ips(sessionId="", assetId=assetId).info(),
            permission={
                "args": {
                    "assetId": assetId
                }
            }
        )



    def put(self, request: Request, assetId: int) -> Response:
        return self.globalRewrite(
            request=request,
            assetId=assetId,
            actionCallback=lambda data: Ips(sessionId=self.sessionId, assetId=assetId).runUpdate(data),
            permission={
                "args": {
                    "assetId": assetId
                }
            }
        )
