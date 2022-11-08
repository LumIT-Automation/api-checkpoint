from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.Role import Role

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetList


class CheckPointRolesController(CustomControllerCheckPointGetList):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="role", *args, **kwargs)



    def get(self, request: Request, assetId: int, domain: str) -> Response:
        def actionCallback():
            localOnly = False
            if "local" in request.GET:
                localOnly = True

            return Role.listQuick(sessionId="", assetId=assetId, domain=domain, localOnly=localOnly)

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
