from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.Task import Task

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetInfo


class CheckPointTaskController(CustomControllerCheckPointGetInfo):
    def __init__(self, *args, **kwargs):
        CustomControllerCheckPointGetInfo.__init__(self, subject="task", *args, **kwargs)


    def get(self, request: Request, assetId: int, domain: str, taskUid: str) -> Response:
        return self.getInfo(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid=taskUid,
            actionCallback=lambda: Task(sessionId="", assetId=assetId, domain=domain, uid=taskUid).info(),
            permission={
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
