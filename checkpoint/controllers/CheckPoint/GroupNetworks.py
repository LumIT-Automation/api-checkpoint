from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.GroupNetwork import GroupNetwork

from checkpoint.serializers.CheckPoint.GroupNetworks import CheckPointGroupNetworksSerializer as Serializer

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetList
from checkpoint.controllers.CustomControllerPost import CustomControllerCheckPointCreate


class CheckPointGroupNetworksController(CustomControllerCheckPointGetList, CustomControllerCheckPointCreate):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="group_network", *args, **kwargs)



    def get(self, request: Request, assetId: int, domain: str, groupUid: str) -> Response:
        return self.getList(
            request=request,
            assetId=assetId,
            domain=domain,
            actionCallback=lambda: GroupNetwork.listGroupNetworks(sessionId="", assetId=assetId, domain=domain, groupUid=groupUid),
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
            actionCallback=lambda data: GroupNetwork.addNetworksToGroup(sessionId=self.sessionId, assetId=assetId, domain=domain, groupUid=groupUid, networkUids=data["networks"]),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
