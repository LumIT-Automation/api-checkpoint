from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.GroupNetwork import GroupNetwork

from checkpoint.controllers.CustomControllerDelete import CustomControllerCheckPointDelete


class CheckPointGroupNetworkController(CustomControllerCheckPointDelete):
    def __init__(self, *args, **kwargs):
        CustomControllerCheckPointDelete.__init__(self, subject="group_network", *args, **kwargs)



    def delete(self, request: Request, assetId: int, domain: str, groupUid: str, networkUid: str) -> Response:
        return self.remove(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=groupUid,
            actionCallback=lambda: GroupNetwork(sessionId=self.sessionId, assetId=assetId, domain=domain, groupUid=groupUid, networkUid=networkUid).remove(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
