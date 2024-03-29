from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.IpsSchedule import IpsSchedule

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetInfo
from checkpoint.controllers.CustomControllerPatch import CustomControllerCheckPointUpdate


class CheckPointIpsScheduleController(CustomControllerCheckPointGetInfo, CustomControllerCheckPointUpdate):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="ips_schedule", *args, **kwargs)



    def get(self, request: Request, assetId: int, domain: str) -> Response:
        return self.getInfo(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid="schedule",
            actionCallback=lambda: IpsSchedule(sessionId="", assetId=assetId, domain=domain).info(),
            permission={
                "args": {
                    "assetId": assetId
                }
            }
        )



    def patch(self, request: Request, assetId: int, domain: str) -> Response:
        return self.modify(
            request=request,
            assetId=assetId,
            domain=domain,
            objectUid="schedule",
            actionCallback=lambda data: IpsSchedule(sessionId=self.sessionId, assetId=assetId, domain=domain).modify(data),
            permission={
                "args": {
                    "assetId": assetId
                }
            }
        )
