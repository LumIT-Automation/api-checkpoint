from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.Group import Group

from checkpoint.serializers.CheckPoint.Group import CheckPointGroupSerializer as Serializer

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetInfo
from checkpoint.controllers.CustomControllerPatch import CustomControllerCheckPointUpdate
from checkpoint.controllers.CustomControllerDelete import CustomControllerCheckPointDelete


class CheckPointGroupController(CustomControllerCheckPointGetInfo, CustomControllerCheckPointUpdate, CustomControllerCheckPointDelete):
    def __init__(self, *args, **kwargs):
        CustomControllerCheckPointGetInfo.__init__(self, subject="group", *args, **kwargs)


    def get(self, request: Request, assetId: int, domain: str, groupUid: str) -> Response:
        return self.getInfo(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=groupUid,
            actionCallback=lambda: Group(sessionId="", assetId=assetId, domain=domain, uid=groupUid).info(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def delete(self, request: Request, assetId: int, domain: str, groupUid: str) -> Response:
        return self.remove(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=groupUid,
            actionCallback=lambda: Group(sessionId=self.sessionId, assetId=assetId, domain=domain, uid=groupUid).delete(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def patch(self, request: Request, assetId: int, domain: str, groupUid: str) -> Response:
        return self.modify(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=groupUid,
            Serializer=Serializer,
            actionCallback=lambda data: Group(sessionId=self.sessionId, assetId=assetId, domain=domain, uid=groupUid).modify(data),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
