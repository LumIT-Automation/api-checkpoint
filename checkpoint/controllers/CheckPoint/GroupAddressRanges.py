from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.GroupAddressRange import GroupAddressRange
from checkpoint.models.Permission.Permission import Permission

from checkpoint.serializers.CheckPoint.GroupAddressRanges import CheckPointGroupAddressRangesSerializer as Serializer


from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetList
from checkpoint.controllers.CustomControllerPost import CustomControllerCheckPointCreate


class CheckPointGroupAddressRangesController(CustomControllerCheckPointGetList, CustomControllerCheckPointCreate):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="group_address_range", *args, **kwargs)



    def get(self, request: Request, assetId: int, domain: str, groupUid: str) -> Response:
        return self.getList(
            request=request,
            assetId=assetId,
            domain=domain,
            containerObjectUid=groupUid,
            actionCallback=lambda: GroupAddressRange.listGroupAddressRanges(sessionId="", assetId=assetId, domain=domain, groupUid=groupUid),
            permission={
                "method": Permission.hasUserPermission,
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
            containerObjectUid=groupUid,
            Serializer=Serializer,
            actionCallback=lambda data: GroupAddressRange.addAddressRangesToGroup(
                sessionId=self.sessionId,
                assetId=assetId,
                domain=domain,
                groupUid=groupUid,
                rangeUids=data["address-ranges"]
            ),
            permission={
                "method": Permission.hasUserPermission,
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
