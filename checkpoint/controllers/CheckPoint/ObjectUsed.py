from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.Object import Object

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetInfo


class CheckPointObjectWhereUsedController(CustomControllerCheckPointGetInfo):
    def __init__(self, *args, **kwargs):
        CustomControllerCheckPointGetInfo.__init__(self, subject="object", *args, **kwargs)


    def get(self, request: Request, assetId: int, domain: str, objectUid: str) -> Response:
        return self.getInfo(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=objectUid,
            actionCallback=lambda: Object(sessionId="", assetId=assetId, domain=domain, uid=objectUid).whereUsed(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
