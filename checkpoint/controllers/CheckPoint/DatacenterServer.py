from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.DatacenterServer import DatacenterServer

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetInfo
from checkpoint.controllers.CustomControllerPatch import CustomControllerCheckPointUpdate
from checkpoint.controllers.CustomControllerDelete import CustomControllerCheckPointDelete


class CheckPointDatacenterServerController(CustomControllerCheckPointGetInfo, CustomControllerCheckPointUpdate, CustomControllerCheckPointDelete):
    def __init__(self, *args, **kwargs):
        CustomControllerCheckPointGetInfo.__init__(self, subject="datacenter_server", *args, **kwargs)


    def get(self, request: Request, assetId: int, domain: str, datacenterUid: str) -> Response:
        return self.getInfo(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=datacenterUid,
            actionCallback=lambda: DatacenterServer(sessionId="", assetId=assetId, domain=domain, uid=datacenterUid).info(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def delete(self, request: Request, assetId: int, domain: str, datacenterUid: str) -> Response:
        return self.remove(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=datacenterUid,
            actionCallback=lambda: DatacenterServer(sessionId=self.sessionId, assetId=assetId, domain=domain, uid=datacenterUid).delete(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def patch(self, request: Request, assetId: int, domain: str, datacenterUid: str) -> Response:
        return self.modify(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=datacenterUid,
            actionCallback=lambda data: DatacenterServer(sessionId=self.sessionId, assetId=assetId, domain=domain, uid=datacenterUid).modify(data),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
