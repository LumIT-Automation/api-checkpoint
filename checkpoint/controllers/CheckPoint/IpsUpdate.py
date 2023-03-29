from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.Ips import Ips

from checkpoint.controllers.CustomControllerPut import CustomControllerCheckPointUpdateAll


class CheckPointIpsUpdateController(CustomControllerCheckPointUpdateAll):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="ips", *args, **kwargs)



    def put(self, request: Request, assetId: int, domain: str) -> Response:
        return self.launchTask(
            request=request,
            assetId=assetId,
            domain=domain,
            actionCallback=lambda data: Ips(sessionId=self.sessionId, assetId=assetId, domain=domain).runUpdate(data),
            permission={
                "args": {
                    "assetId": assetId
                }
            }
        )
