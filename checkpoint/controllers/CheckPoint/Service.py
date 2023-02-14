from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.Service import Service

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetInfo
from checkpoint.controllers.CustomControllerPatch import CustomControllerCheckPointUpdate
from checkpoint.controllers.CustomControllerDelete import CustomControllerCheckPointDelete


class CheckPointServiceController(CustomControllerCheckPointGetInfo, CustomControllerCheckPointUpdate, CustomControllerCheckPointDelete):
    def __init__(self, serviceType: str, *args, **kwargs):
        CustomControllerCheckPointGetInfo.__init__(self, subject="service", *args, **kwargs)

        self.serviceType = serviceType



    def get(self, request: Request, assetId: int, domain: str, serviceUid: str) -> Response:
        return self.getInfo(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=serviceUid,
            objectType=self.serviceType,
            actionCallback=lambda: Service(sessionId="", serviceType=self.serviceType, assetId=assetId, domain=domain, uid=serviceUid).info(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def delete(self, request: Request, assetId: int, domain: str, serviceUid: str) -> Response:
        return self.remove(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=serviceUid,
            objectType=self.serviceType,
            actionCallback=lambda: Service(sessionId=self.sessionId, serviceType=self.serviceType, assetId=assetId, domain=domain, uid=serviceUid).delete(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def patch(self, request: Request, assetId: int, domain: str, serviceUid: str) -> Response:
        def actionCallback(data):
            Service(sessionId=self.sessionId, serviceType=self.serviceType, assetId=assetId, domain=domain, uid=serviceUid).modify(data)

        return self.modify(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=serviceUid,
            objectType=self.serviceType,
            actionCallback=actionCallback,
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
