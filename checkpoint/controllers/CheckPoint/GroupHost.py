from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.GroupHost import GroupHost

from checkpoint.controllers.CustomControllerDelete import CustomControllerCheckPointDelete


class CheckPointGroupHostController(CustomControllerCheckPointDelete):
    def __init__(self, *args, **kwargs):
        CustomControllerCheckPointDelete.__init__(self, subject="group_host", *args, **kwargs)



    def delete(self, request: Request, assetId: int, domain: str, groupUid: str, hostUid: str) -> Response:
        return self.remove(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=groupUid,
            actionCallback=lambda: GroupHost(sessionId=self.sessionId, assetId=assetId, domain=domain, groupUid=groupUid, hostUid=hostUid).remove(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
