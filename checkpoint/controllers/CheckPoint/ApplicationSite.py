from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.ApplicationSite import ApplicationSite

from checkpoint.serializers.CheckPoint.ApplicationSite import CheckPointApplicationSiteSerializer as Serializer

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetInfo
from checkpoint.controllers.CustomControllerPatch import CustomControllerCheckPointUpdate
from checkpoint.controllers.CustomControllerDelete import CustomControllerCheckPointDelete


class CheckPointApplicationSiteController(CustomControllerCheckPointGetInfo, CustomControllerCheckPointUpdate, CustomControllerCheckPointDelete):
    def __init__(self, *args, **kwargs):
        CustomControllerCheckPointGetInfo.__init__(self, subject="application_site", *args, **kwargs)


    def get(self, request: Request, assetId: int, domain: str, appSiteUid: str) -> Response:
        return self.getInfo(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=appSiteUid,
            actionCallback=lambda: ApplicationSite(sessionId="", assetId=assetId, domain=domain, uid=appSiteUid).info(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def delete(self, request: Request, assetId: int, domain: str, appSiteUid: str) -> Response:
        return self.remove(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=appSiteUid,
            actionCallback=lambda: ApplicationSite(sessionId=self.sessionId, assetId=assetId, domain=domain, uid=appSiteUid).delete(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def patch(self, request: Request, assetId: int, domain: str, appSiteUid: str) -> Response:
        return self.modify(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=appSiteUid,
            Serializer=Serializer,
            actionCallback=lambda data: ApplicationSite(sessionId=self.sessionId, assetId=assetId, domain=domain, uid=appSiteUid).modify(data),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
