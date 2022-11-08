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


class CustomControllerCheckPointCreate(CustomControllerBase):
    def __init__(self,  subject: str, *args, **kwargs):
        self.sessionId = uuid.uuid4().hex
        self.subject = subject



    def create(self, request: Request, permission: dict, actionCallback: Callable, Serializer: Callable, assetId: int = 0, domain: str = "", objectType: str = "", containerObjectUid: str = "") -> Response:
        if self.subject[-1:] == "y":
            action = self.subject[:-1] + "ies_post"
        else:
            action = self.subject + "s_post"
        actionLog = f"{self.subject.capitalize()} {objectType} - addition: {domain}".replace("  ", " ")
        lockedObjectClass = self.subject + objectType

        response = dict()

        try:
            user = CustomControllerBase.loggedUser(request)
            # Check if user has permission of doing <action> on asset (if specified) and partition (if specified).
            if Permission.hasUserPermission(groups=user["groups"], action=action, **permission["args"]) or user["authDisabled"]:
                Log.actionLog(actionLog, user)
                Log.actionLog("User data: " + str(request.data), user)

                serializer = Serializer(data=request.data["data"])
                if serializer.is_valid():
                    data = serializer.validated_data

                    # [no containerObjectUid specified] Locking logic for a class of objects, for example: group:POST:1:POLAND = 'any'.
                    # [containerObjectUid specified] Locking logic for a class of objects contained within the containerObject, example: hosts within a group: group_host:POST:1:POLAND = ' ID'.
                    # A type can also be specified (example: layeraccess:POST:1:POLAND = 'any').
                    lock = Lock(lockedObjectClass, locals(), containerObjectUid)
                    if lock.isUnlocked():
                        lock.lock()

                        response["data"] = actionCallback(data)
                        if not response["data"]:
                            response = None
                        httpStatus = status.HTTP_201_CREATED

                        lock.release()
                    else:
                        httpStatus = status.HTTP_423_LOCKED
                else:
                    httpStatus = status.HTTP_400_BAD_REQUEST
                    response = {
                        "CheckPoint": {
                            "error": str(serializer.errors)
                        }
                    }
                    Log.actionLog("User data incorrect: " + str(response), user)
            else:
                response = None
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            Lock(lockedObjectClass, locals(), locals()["containerObjectUid"]).release()

            data, httpStatus, headers = CustomControllerBase.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)
        finally:
            try:
                if assetId:
                    if httpStatus != status.HTTP_423_LOCKED and httpStatus != status.HTTP_400_BAD_REQUEST and httpStatus != status.HTTP_403_FORBIDDEN:
                        time.sleep(0.5) # oh gosh.
                        Session(sessionId=self.sessionId, assetId=assetId, domain=domain).logout() # logout from CheckPoint.
            except Exception:
                pass

        return Response(response, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
