from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.ApplicationSiteCategory import ApplicationSiteCategory

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetInfo
from checkpoint.controllers.CustomControllerPatch import CustomControllerCheckPointUpdate
from checkpoint.controllers.CustomControllerDelete import CustomControllerCheckPointDelete


class CheckPointApplicationSiteCategoryController(CustomControllerCheckPointGetInfo, CustomControllerCheckPointUpdate, CustomControllerCheckPointDelete):
    def __init__(self, *args, **kwargs):
        CustomControllerCheckPointGetInfo.__init__(self, subject="host", *args, **kwargs)


    def get(self, request: Request, assetId: int, domain: str, categoryUid: str) -> Response:
        return self.getInfo(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=categoryUid,
            actionCallback=lambda: ApplicationSiteCategory(sessionId="", assetId=assetId, domain=domain, uid=categoryUid).info(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def delete(self, request: Request, assetId: int, domain: str, categoryUid: str) -> Response:
        return self.remove(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=categoryUid,
            actionCallback=lambda: ApplicationSiteCategory(sessionId=self.sessionId, assetId=assetId, domain=domain, uid=categoryUid).delete(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def patch(self, request: Request, assetId: int, domain: str, categoryUid: str) -> Response:
        return self.modify(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=categoryUid,
            actionCallback=lambda data: ApplicationSiteCategory(sessionId=self.sessionId, assetId=assetId, domain=domain, uid=categoryUid).modify(data),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
