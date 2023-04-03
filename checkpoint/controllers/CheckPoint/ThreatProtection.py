from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.ThreatProtection import ThreatProtection

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetInfo
from checkpoint.controllers.CustomControllerPatch import CustomControllerCheckPointUpdate
from checkpoint.controllers.CustomControllerDelete import CustomControllerCheckPointDelete


class CheckPointThreatProtectionController(CustomControllerCheckPointGetInfo, CustomControllerCheckPointUpdate, CustomControllerCheckPointDelete):
    def __init__(self, *args, **kwargs):
        CustomControllerCheckPointGetInfo.__init__(self, subject="threat_protection", *args, **kwargs)

    def get(self, request: Request, assetId: int, domain: str, threatProtectionUid: str) -> Response:
        return self.getInfo(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=threatProtectionUid,
            actionCallback=lambda: ThreatProtection(sessionId="", assetId=assetId, domain=domain, uid=threatProtectionUid).info(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def patch(self, request: Request, assetId: int, domain: str, threatProtectionUid: str) -> Response:
        return self.modify(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=threatProtectionUid,
            actionCallback=lambda data: ThreatProtection(sessionId=self.sessionId, assetId=assetId, domain=domain, uid=threatProtectionUid).modify(data),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
