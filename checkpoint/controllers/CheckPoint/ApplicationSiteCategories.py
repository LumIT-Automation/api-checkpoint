from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.ApplicationSiteCategory import ApplicationSiteCategory

from checkpoint.serializers.CheckPoint.ApplicationSiteCategory import CheckPointApplicationSiteCategorySerializer as Serializer

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetList
from checkpoint.controllers.CustomControllerPost import CustomControllerCheckPointCreate


class CheckPointApplicationSiteCategoriesController(CustomControllerCheckPointGetList, CustomControllerCheckPointCreate):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="application_site_category", *args, **kwargs)



    def get(self, request: Request, assetId: int, domain: str) -> Response:
        return self.getList(
            request=request,
            assetId=assetId,
            domain=domain,
            actionCallback=lambda: ApplicationSiteCategory.listQuick(sessionId="", assetId=assetId, domain=domain),
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
            Serializer=Serializer,
            actionCallback=lambda data: ApplicationSiteCategory.add(sessionId=self.sessionId, assetId=assetId, domain=domain, data=data),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
