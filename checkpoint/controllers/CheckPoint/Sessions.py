from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.Session import Session
from checkpoint.models.Permission.Permission import Permission

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetList


class CheckPointSessionsController(CustomControllerCheckPointGetList):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="session", *args, **kwargs)



    def get(self, request: Request, assetId: int, domain: str = "") -> Response:
        def actionCallback():
            detailsLevel = "standard"
            if "fullDetails" in request.GET:
                detailsLevel = "full"

            return Session.listQuick(sessionId="", assetId=assetId, domain=domain, details=detailsLevel)

        return self.getList(
            request=request,
            assetId=assetId,
            domain=domain,
            actionCallback=actionCallback,
            permission={
                "method": Permission.hasUserPermission,
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
