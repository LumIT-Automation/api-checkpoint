from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.ApplicationSite import ApplicationSite
from checkpoint.models.Permission.Permission import Permission

from checkpoint.serializers.CheckPoint.ApplicationSite import CheckPointApplicationSiteSerializer as Serializer

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetList
from checkpoint.controllers.CustomControllerPost import CustomControllerCheckPointCreate


class CheckPointApplicationSitesController(CustomControllerCheckPointGetList, CustomControllerCheckPointCreate):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="application_site", *args, **kwargs)



    def get(self, request: Request, assetId: int, domain: str) -> Response:
        def actionCallback():
            localOnly = False
            if "local" in request.GET:
                localOnly = True

            if "custom" in request.GET:
                return ApplicationSite.listCustomApplicationSitesQuick(sessionId="", assetId=assetId, domain=domain, localOnly=localOnly)
            else:
                return ApplicationSite.listQuick(sessionId="", assetId=assetId, domain=domain, localOnly=localOnly)

        return self.getList(
            request=request,
            assetId=assetId,
            domain=domain,
            actionCallback=actionCallback,
            permission={
                "method": Permission.hasUserPermission,
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
            Serializer=Serializer,
            actionCallback=lambda data: ApplicationSite.add(sessionId=self.sessionId, assetId=assetId, domain=domain, data=data),
            permission={
                "method": Permission.hasUserPermission,
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
