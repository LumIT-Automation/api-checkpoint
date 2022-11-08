from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.PolicyPackage import PolicyPackage

from checkpoint.serializers.CheckPoint.PolicyPackage import CheckPointPolicyPackageSerializer as Serializer

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetInfo
from checkpoint.controllers.CustomControllerPatch import CustomControllerCheckPointUpdate
from checkpoint.controllers.CustomControllerDelete import CustomControllerCheckPointDelete


class CheckPointPolicyPackageController(CustomControllerCheckPointGetInfo, CustomControllerCheckPointUpdate, CustomControllerCheckPointDelete):
    def __init__(self, *args, **kwargs):
        CustomControllerCheckPointGetInfo.__init__(self, subject="policy_package", *args, **kwargs)


    def get(self, request: Request, assetId: int, domain: str, packageUid: str) -> Response:
        return self.getInfo(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=packageUid,
            actionCallback=lambda: PolicyPackage(sessionId="", assetId=assetId, domain=domain, uid=packageUid).info(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def delete(self, request: Request, assetId: int, domain: str, packageUid: str) -> Response:
        return self.remove(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=packageUid,
            actionCallback=lambda: PolicyPackage(sessionId=self.sessionId, assetId=assetId, domain=domain, uid=packageUid).delete(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def patch(self, request: Request, assetId: int, domain: str, packageUid: str) -> Response:
        return self.modify(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=packageUid,
            Serializer=Serializer,
            actionCallback=lambda data: PolicyPackage(sessionId=self.sessionId, assetId=assetId, domain=domain, uid=packageUid).modify(data),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
