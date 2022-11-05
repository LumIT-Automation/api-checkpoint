import uuid
import time

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from checkpoint.models.CheckPoint.Group import Group
from checkpoint.models.CheckPoint.Session import Session
from checkpoint.models.Permission.Permission import Permission

from checkpoint.controllers.CustomControllerBase import CustomControllerBase

from checkpoint.helpers.Lock import Lock
from checkpoint.helpers.Log import Log


class CheckPointGroupGroupController(CustomControllerBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = uuid.uuid4().hex



    def delete(self, request: Request, assetId: int, domain: str, groupUid: str, childGroupUid: str) -> Response:
        user = CustomControllerBase.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="group_delete", assetId=assetId) or user["authDisabled"]:
                Log.actionLog("Group inner group removal", user)

                lock = Lock("Group", locals(), groupUid)
                if lock.isUnlocked():
                    lock.lock()

                    Group(sessionId=self.sessionId, assetId=assetId, domain=domain, uid=groupUid).deleteInnerGroup(childGroupUid)
                    httpStatus = status.HTTP_200_OK
                    lock.release()
                else:
                    httpStatus = status.HTTP_423_LOCKED
            else:
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            Lock("group", locals(), locals()["groupUid"]).release()

            data, httpStatus, headers = CustomControllerBase.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)
        finally:
            try:
                time.sleep(0.5)
                Session(sessionId=self.sessionId, assetId=assetId, domain=domain).logout()
            except Exception:
                pass

        return Response(None, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
