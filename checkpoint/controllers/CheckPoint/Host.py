from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.Host import Host

from checkpoint.serializers.CheckPoint.Host import CheckPointHostSerializer as Serializer

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetInfo
from checkpoint.controllers.CustomControllerPatch import CustomControllerCheckPointUpdate
from checkpoint.controllers.CustomControllerDelete import CustomControllerCheckPointDelete


class CheckPointHostController(CustomControllerCheckPointGetInfo, CustomControllerCheckPointUpdate, CustomControllerCheckPointDelete):
    def __init__(self, *args, **kwargs):
        CustomControllerCheckPointGetInfo.__init__(self, subject="host", *args, **kwargs)


    def get(self, request: Request, assetId: int, domain: str, hostUid: str) -> Response:
        return self.getInfo(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=hostUid,
            actionCallback=lambda: Host(sessionId="", assetId=assetId, domain=domain, uid=hostUid).info(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def delete(self, request: Request, assetId: int, domain: str, hostUid: str) -> Response:
        return self.remove(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=hostUid,
            actionCallback=lambda: Host(sessionId=self.sessionId, assetId=assetId, domain=domain, uid=hostUid).delete(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def patch(self, request: Request, assetId: int, domain: str, hostUid: str) -> Response:
        return self.modify(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=hostUid,
            Serializer=Serializer,
            actionCallback=lambda data: Host(sessionId=self.sessionId, assetId=assetId, domain=domain, uid=hostUid).modify(data),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
