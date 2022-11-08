from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.Object import Object

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetList


class CheckPointObjectsUnusedController(CustomControllerCheckPointGetList):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="object", *args, **kwargs)



    def get(self, request: Request, assetId: int, domain: str) -> Response:
        return self.getList(
            request=request,
            assetId=assetId,
            domain=domain,
            actionCallback=lambda: Object.listUnused(sessionId="", assetId=assetId, domain=domain),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
