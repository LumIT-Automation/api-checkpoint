from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.GroupHost import GroupHost

from checkpoint.serializers.CheckPoint.GroupHosts import CheckPointGroupHostsSerializer as Serializer

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetList
from checkpoint.controllers.CustomControllerPost import CustomControllerCheckPointCreate


class CheckPointGroupHostsController(CustomControllerCheckPointGetList, CustomControllerCheckPointCreate):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="group_host", *args, **kwargs)



    def get(self, request: Request, assetId: int, domain: str, groupUid: str) -> Response:
        return self.getList(
            request=request,
            assetId=assetId,
            domain=domain,
            actionCallback=lambda: GroupHost.listGroupHosts(sessionId="", assetId=assetId, domain=domain, groupUid=groupUid),
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
            actionCallback=lambda data: GroupHost.addHostsToGroup(sessionId=self.sessionId, assetId=assetId, domain=domain, groupUid=groupUid, hostUids=data["hosts"]),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
