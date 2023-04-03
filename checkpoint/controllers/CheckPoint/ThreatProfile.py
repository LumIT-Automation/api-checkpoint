from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.ThreatProfile import ThreatProfile

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetInfo
from checkpoint.controllers.CustomControllerPatch import CustomControllerCheckPointUpdate
from checkpoint.controllers.CustomControllerDelete import CustomControllerCheckPointDelete


class CheckPointThreatProfileController(CustomControllerCheckPointGetInfo, CustomControllerCheckPointUpdate, CustomControllerCheckPointDelete):
    def __init__(self, *args, **kwargs):
        CustomControllerCheckPointGetInfo.__init__(self, subject="threat_profile", *args, **kwargs)

    def get(self, request: Request, assetId: int, domain: str, threatProfileUid: str) -> Response:
        return self.getInfo(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=threatProfileUid,
            actionCallback=lambda: ThreatProfile(sessionId="", assetId=assetId, domain=domain, uid=threatProfileUid).info(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def delete(self, request: Request, assetId: int, domain: str, threatProfileUid: str) -> Response:
        return self.remove(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=threatProfileUid,
            actionCallback=lambda: ThreatProfile(sessionId="", assetId=assetId, domain=domain, uid=threatProfileUid).delete(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def patch(self, request: Request, assetId: int, domain: str, threatProfileUid: str) -> Response:
        return self.modify(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=threatProfileUid,
            actionCallback=lambda data: ThreatProfile(sessionId=self.sessionId, assetId=assetId, domain=domain, uid=threatProfileUid).modify(data),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
