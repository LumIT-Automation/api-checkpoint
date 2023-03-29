from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.Ips import Ips

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetList


class CheckPointIpsExtendedAttributesController(CustomControllerCheckPointGetList):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="ips_attribute", *args, **kwargs)



    def get(self, request: Request, assetId: int, domain: str) -> Response:
        return self.getList(
            request=request,
            assetId=assetId,
            actionCallback=lambda: Ips.listExtendedAttributes(sessionId=self.sessionId, assetId=assetId, domain=domain),
            permission={
                "args": {
                    "assetId": assetId
                }
            }
        )
