from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.Group import Group

from checkpoint.controllers.CustomControllerDelete import CustomControllerCheckPointDelete


class CheckPointGroupGroupController(CustomControllerCheckPointDelete):
    def __init__(self, *args, **kwargs):
        CustomControllerCheckPointDelete.__init__(self, subject="group", *args, **kwargs)



    def delete(self, request: Request, assetId: int, domain: str, groupUid: str, childGroupUid: str) -> Response:
        return self.remove(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=groupUid,
            actionCallback=lambda: Group(sessionId=self.sessionId, assetId=assetId, domain=domain, uid=groupUid).deleteInnerGroup(childGroupUid),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
