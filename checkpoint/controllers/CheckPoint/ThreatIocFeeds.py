from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.ThreatIocFeed import ThreatIocFeed

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetList
from checkpoint.controllers.CustomControllerPost import CustomControllerCheckPointCreate


class CheckPointThreatIocFeedsController(CustomControllerCheckPointGetList, CustomControllerCheckPointCreate):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="threat_iov_feed", *args, **kwargs)

    def get(self, request: Request, assetId: int, domain: str) -> Response:
        def actionCallback():
            localOnly = False
            if "local" in request.GET:
                localOnly = True

            return ThreatIocFeed.listQuick(sessionId="", assetId=assetId, domain=domain, localOnly=localOnly)

        return self.getList(
            request=request,
            assetId=assetId,
            domain=domain,
            actionCallback=actionCallback,
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def post(self, request: Request, assetId: int, domain: str) -> Response:
        return self.create(
            request=request,
            assetId=assetId,
            domain=domain,
            actionCallback=lambda data: ThreatIocFeed.add(sessionId=self.sessionId, assetId=assetId, domain=domain, data=data),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
