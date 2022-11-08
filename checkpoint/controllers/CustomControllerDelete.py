import uuid
import time
from typing import Callable

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from checkpoint.models.Permission.Permission import Permission
from checkpoint.models.CheckPoint.Session import Session

from checkpoint.controllers.CustomControllerBase import CustomControllerBase

from checkpoint.helpers.Lock import Lock
from checkpoint.helpers.Log import Log


class CustomControllerCheckPointDelete(CustomControllerBase):
    def __init__(self,  subject: str, *args, **kwargs):
        self.sessionId = uuid.uuid4().hex
        self.subject = subject



    def remove(self, request: Request, permission: dict, actionCallback: Callable, objectUid: str, assetId: int = 0, domain: str = "", objectType: str = "") -> Response:
        action = self.subject + "_delete"
        actionLog = f"{self.subject.capitalize()} {objectType} - deletion: {domain} {objectUid}".replace("  ", " ")
        lockedObjectClass = self.subject + objectType

        # Example:
        #   subject: host
        #   action: host_delete
        #   lockedObjectClass: host

        try:
            user = CustomControllerBase.loggedUser(request)
            # Check if user has permission of doing <action> on asset (if specified) and partition (if specified).
            if Permission.hasUserPermission(groups=user["groups"], action=action, **permission["args"]) or user["authDisabled"]:
                Log.actionLog(actionLog, user)

                # Locking logic for a specific object, example: host:DELETE:1:DOMAIN = 'objectUid',
                # @todo: locking logic for all object's fathers should be applied, too: object -> whereUsed() -> lock.

                lock = Lock(lockedObjectClass, locals(), objectUid)
                if lock.isUnlocked():
                    lock.lock()

                    actionCallback()
                    httpStatus = status.HTTP_200_OK

                    lock.release()
                else:
                    data = None
                    httpStatus = status.HTTP_423_LOCKED
            else:
                data = None
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            Lock(lockedObjectClass, locals(), objectUid).release()

            data, httpStatus, headers = CustomControllerBase.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)
        finally:
            try:
                if assetId:
                    if httpStatus != status.HTTP_423_LOCKED and httpStatus != status.HTTP_403_FORBIDDEN:
                        time.sleep(0.5)
                        Session(sessionId=self.sessionId, assetId=assetId, domain=domain).logout()
            except Exception:
                pass

        return Response(None, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
