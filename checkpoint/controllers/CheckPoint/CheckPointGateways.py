from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.CheckPointGateway import CheckPointGateway

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetList


class CheckPointGatewaysController(CustomControllerCheckPointGetList):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="checkpoint_gateway", *args, **kwargs)



    def get(self, request: Request, assetId: int) -> Response:
        return self.getList(
            request=request,
            assetId=assetId,
            actionCallback=lambda: CheckPointGateway.listQuick(sessionId="", assetId=assetId),
            permission={
                "args": {
                    "assetId": assetId
                }
            }
        )
