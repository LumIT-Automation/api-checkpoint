from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.Ips import Ips

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetInfo


class CheckPointIpsExtendedAttributeController(CustomControllerCheckPointGetInfo):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="ips", *args, **kwargs)



    def get(self, request: Request, assetId: int, domain: str, attributeUid) -> Response:
        return self.getInfo(
            request=request,
            assetId=assetId,
            objectUid=attributeUid,
            actionCallback=lambda: Ips(sessionId=self.sessionId, assetId=assetId, domain=domain).extendedAttributeInfo(attributeUid=attributeUid),
            permission={
                "args": {
                    "assetId": assetId
                }
            }
        )
