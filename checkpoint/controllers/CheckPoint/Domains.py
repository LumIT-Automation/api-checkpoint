from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.Domain import Domain

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetList


class CheckPointDomainsController(CustomControllerCheckPointGetList):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="domain", *args, **kwargs)



    def get(self, request: Request, assetId: int) -> Response:
        return self.getList(
            request=request,
            assetId=assetId,
            actionCallback=lambda: Domain.listQuick(sessionId="", assetId=assetId),
            permission={
                "args": {
                    "assetId": assetId
                }
            }
        )
