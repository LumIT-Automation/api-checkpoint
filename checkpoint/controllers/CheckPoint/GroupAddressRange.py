from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.GroupAddressRange import GroupAddressRange
from checkpoint.models.Permission.Permission import Permission

from checkpoint.controllers.CustomControllerDelete import CustomControllerCheckPointDelete


class CheckPointGroupAddressRangeController(CustomControllerCheckPointDelete):
    def __init__(self, *args, **kwargs):
        CustomControllerCheckPointDelete.__init__(self, subject="group_address_range", *args, **kwargs)


    def delete(self, request: Request, assetId: int, domain: str, groupUid: str, rangeUid: str) -> Response:
        return self.remove(
            request=request,
            assetId=assetId,
            domain=domain,
            obj={
                "uid": rangeUid,
                "containerUid": groupUid
            },
            actionCallback=lambda: GroupAddressRange(sessionId=self.sessionId, assetId=assetId, domain=domain, groupUid=groupUid, rangeUid=rangeUid).remove(),
            permission={
                "method": Permission.hasUserPermission,
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
