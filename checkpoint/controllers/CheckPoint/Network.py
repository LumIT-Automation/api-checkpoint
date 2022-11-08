from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.Network import Network

from checkpoint.serializers.CheckPoint.Network import CheckPointNetworkSerializer as Serializer

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetInfo
from checkpoint.controllers.CustomControllerPatch import CustomControllerCheckPointUpdate
from checkpoint.controllers.CustomControllerDelete import CustomControllerCheckPointDelete


class CheckPointNetworkController(CustomControllerCheckPointGetInfo, CustomControllerCheckPointUpdate, CustomControllerCheckPointDelete):
    def __init__(self, *args, **kwargs):
        CustomControllerCheckPointGetInfo.__init__(self, subject="network", *args, **kwargs)

    def get(self, request: Request, assetId: int, domain: str, networkUid: str) -> Response:
        return self.getInfo(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=networkUid,
            actionCallback=lambda: Network(sessionId="", assetId=assetId, domain=domain, uid=networkUid).info(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def delete(self, request: Request, assetId: int, domain: str, networkUid: str) -> Response:
        return self.remove(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=networkUid,
            actionCallback=lambda: Network(sessionId=self.sessionId, assetId=assetId, domain=domain, uid=networkUid).delete(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def patch(self, request: Request, assetId: int, domain: str, networkUid: str) -> Response:
        return self.modify(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=networkUid,
            Serializer=Serializer,
            actionCallback=lambda data: Network(sessionId=self.sessionId, assetId=assetId, domain=domain, uid=networkUid).modify(data),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
