from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.ThreatIocFeed import ThreatIocFeed

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetInfo
from checkpoint.controllers.CustomControllerPatch import CustomControllerCheckPointUpdate
from checkpoint.controllers.CustomControllerDelete import CustomControllerCheckPointDelete


class CheckPointThreatIocFeedController(CustomControllerCheckPointGetInfo, CustomControllerCheckPointUpdate, CustomControllerCheckPointDelete):
    def __init__(self, *args, **kwargs):
        CustomControllerCheckPointGetInfo.__init__(self, subject="threat_ioc_feed", *args, **kwargs)

    def get(self, request: Request, assetId: int, domain: str, threatIocFeedUid: str) -> Response:
        return self.getInfo(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=threatIocFeedUid,
            actionCallback=lambda: ThreatIocFeed(sessionId="", assetId=assetId, domain=domain, uid=threatIocFeedUid).info(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def delete(self, request: Request, assetId: int, domain: str, threatIocFeedUid: str) -> Response:
        return self.remove(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=threatIocFeedUid,
            actionCallback=lambda: ThreatIocFeed(sessionId="", assetId=assetId, domain=domain, uid=threatIocFeedUid).delete(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def patch(self, request: Request, assetId: int, domain: str, threatIocFeedUid: str) -> Response:
        return self.modify(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=threatIocFeedUid,
            actionCallback=lambda data: ThreatIocFeed(sessionId=self.sessionId, assetId=assetId, domain=domain, uid=threatIocFeedUid).modify(data),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
