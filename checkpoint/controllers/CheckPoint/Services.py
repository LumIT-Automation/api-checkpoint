from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.Service import Service

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetList
from checkpoint.controllers.CustomControllerPost import CustomControllerCheckPointCreate


class CheckPointServicesController(CustomControllerCheckPointGetList, CustomControllerCheckPointCreate):
    def __init__(self, serviceType: str, *args, **kwargs):
        super().__init__(subject="service", *args, **kwargs)

        self.serviceType = serviceType



    def get(self, request: Request, assetId: int, domain: str) -> Response:
        def actionCallback():
            localOnly = False
            if "local" in request.GET:
                localOnly = True

            return Service.listQuick(sessionId="", serviceType=self.serviceType, assetId=assetId, domain=domain, localOnly=localOnly)

        return self.getList(
            request=request,
            assetId=assetId,
            domain=domain,
            objectType=self.serviceType,
            actionCallback=actionCallback,
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def post(self, request: Request, assetId: int, domain: str) -> Response:
        def actionCallback(data):
            return Service.add(sessionId=self.sessionId, serviceType=self.serviceType, assetId=assetId, domain=domain, data=data)

        return self.create(
            request=request,
            assetId=assetId,
            domain=domain,
            objectType=self.serviceType,
            actionCallback=actionCallback,
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
