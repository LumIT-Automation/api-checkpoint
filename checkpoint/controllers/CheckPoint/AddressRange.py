from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.AddressRange import AddressRange

from checkpoint.serializers.CheckPoint.AddressRange import CheckPointAddressRangeSerializer as Serializer


from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetInfo
from checkpoint.controllers.CustomControllerPatch import CustomControllerCheckPointUpdate
from checkpoint.controllers.CustomControllerDelete import CustomControllerCheckPointDelete


class CheckPointAddressRangeController(CustomControllerCheckPointGetInfo, CustomControllerCheckPointUpdate, CustomControllerCheckPointDelete):
    def __init__(self, *args, **kwargs):
        CustomControllerCheckPointGetInfo.__init__(self, subject="address_range", *args, **kwargs)


    def get(self, request: Request, assetId: int, domain: str, rangeUid: str) -> Response:
        return self.getInfo(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=rangeUid,
            actionCallback=lambda: AddressRange(sessionId="", assetId=assetId, domain=domain, uid=rangeUid).info(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def delete(self, request: Request, assetId: int, domain: str, rangeUid: str) -> Response:
        return self.remove(
            request=request,
            assetId=assetId,
            domain=domain,
            obj={
                "uid": rangeUid
            },
            actionCallback=lambda: AddressRange(sessionId=self.sessionId, assetId=assetId, domain=domain, uid=rangeUid).delete(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def patch(self, request: Request, assetId: int, domain: str, rangeUid: str) -> Response:
        return self.modify(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=rangeUid,
            Serializer=Serializer,
            actionCallback=lambda data: AddressRange(sessionId=self.sessionId, assetId=assetId, domain=domain, uid=rangeUid).modify(data),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
