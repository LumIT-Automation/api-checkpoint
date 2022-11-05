import uuid
import time
from typing import Callable

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from checkpoint.models.CheckPoint.Session import Session

from checkpoint.controllers.CustomControllerBase import CustomControllerBase

from checkpoint.helpers.Lock import Lock
from checkpoint.helpers.Log import Log


class CustomControllerCheckPointDelete(CustomControllerBase):
    def __init__(self,  subject: str, *args, **kwargs):
        self.sessionId = uuid.uuid4().hex
        self.subject = subject



    def remove(self, request: Request, permission: dict, actionCallback: Callable, obj: dict, assetId: int = 0, domain: str = "") -> Response:
        objectUid = obj.get("uid", "")
        objectClass = obj.get("class", "")

        containerObjectUid = obj.get("containerUid", "")
        containerObjectType = obj.get("containerType", "")

        action = self.subject + "_delete"
        actionLog = f"{self.subject.capitalize()} {objectClass} - deletion: {domain} {objectUid}".replace("  ", " ")

        lockedObject = self.subject + objectClass
        lockedContainerObject = containerObjectType

        try:
            user = CustomControllerBase.loggedUser(request)
            permissionMethod = permission["method"]

            if permissionMethod(groups=user["groups"], action=action, **permission["args"]) or user["authDisabled"]:
                Log.actionLog(actionLog, user)

                # [no containerObjectUid specified] Locking logic for a specific object, for example: host:DELETE:1:POLAND = 'objectUid'.
                # [containerObjectUid specified] Additional locking logic for the container object, example: group:DELETE:1:POLAND = 'containerObjectUid'.
                # @todo: should be done on all object's containers: an object should always provide its containers ("whereused").
                # A class can also be specified (example: layeraccess:DELETE:1:POLAND = 'any').
                olock = Lock(lockedObject, locals(), objectUid)
                clock = Lock(lockedContainerObject, locals(), containerObjectUid)
                if olock.isUnlocked() and clock.isUnlocked():
                    olock.lock()
                    clock.lock() # if lockedContainerObject empty, no action is performed.

                    actionCallback()
                    httpStatus = status.HTTP_200_OK

                    olock.release()
                    clock.release()
                else:
                    data = None
                    httpStatus = status.HTTP_423_LOCKED
            else:
                data = None
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            Lock(lockedObject, locals(), locals()["objectUid"]).release()
            Lock(lockedContainerObject, locals(), locals()["containerObjectUid"]).release()

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
