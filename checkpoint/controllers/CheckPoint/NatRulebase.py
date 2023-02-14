from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.PolicyPackage import PolicyPackage

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetList
from checkpoint.controllers.CustomControllerPost import CustomControllerCheckPointCreate


class CheckPointNatRulebaseController(CustomControllerCheckPointGetList, CustomControllerCheckPointCreate):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="nat_rulebase", *args, **kwargs)



    def get(self, request: Request, assetId: int, domain: str, packageUid: str) -> Response:
        def actionCallback():
            localOnly = False
            if "local" in request.GET:
                localOnly = True

            return PolicyPackage.listNatRules(sessionId="", assetId=assetId, domain=domain, policyPackageUid=packageUid, localOnly=localOnly)

        return self.getList(
            request=request,
            assetId=assetId,
            domain=domain,
            actionCallback=actionCallback,
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def post(self, request: Request, assetId: int, domain: str, packageUid: str) -> Response:
        return self.create(
            request=request,
            assetId=assetId,
            domain=domain,
            actionCallback=lambda data: PolicyPackage.addNatRule(sessionId=self.sessionId, assetId=assetId, domain=domain, policyPackageUid=packageUid, data=data),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
