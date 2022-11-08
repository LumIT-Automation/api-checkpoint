from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.Group import Group

from checkpoint.serializers.CheckPoint.GroupGroups import CheckPointGroupGroupsSerializer as Serializer

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetList
from checkpoint.controllers.CustomControllerPost import CustomControllerCheckPointCreate


class CheckPointGroupGroupsController(CustomControllerCheckPointGetList, CustomControllerCheckPointCreate):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="group", *args, **kwargs)



    def get(self, request: Request, assetId: int, domain: str, groupUid: str) -> Response:
        return self.getList(
            request=request,
            assetId=assetId,
            domain=domain,
            actionCallback=lambda: Group(sessionId="", assetId=assetId, domain=domain, uid=groupUid).listInnerGroups(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def post(self, request: Request, assetId: int, domain: str, groupUid: str) -> Response:
        return self.create(
            request=request,
            assetId=assetId,
            domain=domain,
            Serializer=Serializer,
            actionCallback=lambda data: Group(sessionId=self.sessionId, assetId=assetId, domain=domain, uid=groupUid).addInnerGroup(data["groups"]),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
