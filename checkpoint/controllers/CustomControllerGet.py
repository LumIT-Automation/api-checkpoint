import uuid
from typing import Callable

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from checkpoint.models.Permission.Permission import Permission

from checkpoint.controllers.CustomControllerBase import CustomControllerBase

from checkpoint.helpers.Lock import Lock
from checkpoint.helpers.Conditional import Conditional
from checkpoint.helpers.Log import Log


########################################################################################################################
# Info
########################################################################################################################

class CustomControllerCheckPointGetInfo(CustomControllerBase):
    def __init__(self, subject: str, *args, **kwargs):
        self.sessionId = uuid.uuid4().hex
        self.subject = subject



    def getInfo(self, request: Request, permission: dict, actionCallback: Callable, objectUid: str, assetId: int = 0, domain: str = "", objectType: str = "", Serializer: Callable = None) -> Response:
        Serializer = Serializer or None

        action = self.subject + "_get" # example: host_get.
        actionLog = f"{self.subject.capitalize()} {objectType} - info {domain} {objectUid}".replace("  ", " ")
        lockedObjectClass = self.subject + objectType # example: host (subject=host) // ruleaccess (subject=rule + type=access).

        # Example:
        #   subject: host
        #   action: host_get
        #   lockedObjectClass: host

        data = dict()
        etagCondition = {"responseEtag": ""}

        try:
            user = CustomControllerBase.loggedUser(request)
            # Check if user has permission of doing <action> on asset (if specified) and domain (if specified).
            if Permission.hasUserPermission(groups=user["groups"], action=action, **permission["args"]) or user["authDisabled"]:
                Log.actionLog(actionLog, user)

                # Locking logic for a specific object, example: host:GET:1:DOMAIN = 'objectUid',
                # @todo: locking logic for all object's fathers should be applied, too: object -> whereUsed() -> lock.

                lock = Lock(lockedObjectClass, locals(), objectUid)
                if lock.isUnlocked():
                    lock.lock()

                    data = {
                        "data": CustomControllerBase.validate(actionCallback(), Serializer),
                        "href": request.get_full_path()
                    }

                    # Check the response's ETag validity (against client request).
                    conditional = Conditional(request)
                    etagCondition = conditional.responseEtagFreshnessAgainstRequest(data["data"])
                    if etagCondition["state"] == "fresh":
                        data = None
                        httpStatus = status.HTTP_304_NOT_MODIFIED
                    else:
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

        return Response(data, status=httpStatus, headers={
            "ETag": etagCondition["responseEtag"],
            "Cache-Control": "must-revalidate"
        })



########################################################################################################################
# List
########################################################################################################################

class CustomControllerCheckPointGetList(CustomControllerBase):
    def __init__(self, subject: str, *args, **kwargs):
        self.sessionId = uuid.uuid4().hex
        self.subject = subject



    def getList(self, request: Request, permission: dict, actionCallback: Callable, assetId: int = 0, domain: str = "", objectType: str = "", Serializer: Callable = None) -> Response:
        Serializer = Serializer or None
        data = dict()
        etagCondition = {"responseEtag": ""}
        
        if self.subject[-1:] == "y":
            action = self.subject[:-1] + "ies_get" # example: categories_get.
        else:
            action = self.subject + "s_get" # example: host_get.
        actionLog = f"{self.subject.capitalize()} {objectType} - list {domain}".replace("  ", " ")
        lockedObjectClass = self.subject + objectType # example: category // layeraccess.
        
        # Example: 
        #   subject: host
        #   action: hosts_get
        #   lockedObjectClass: host

        try:
            user = CustomControllerBase.loggedUser(request)
            # Check if user has permission of doing <action> on asset (if specified) and domain (if specified).
            if Permission.hasUserPermission(groups=user["groups"], action=action, **permission["args"]) or user["authDisabled"]:
                Log.actionLog(actionLog, user)

                # Locking logic for a class of objects, for example: host:GET:1:DOMAIN = 'any'.
                # @todo: locking logic for all object's fathers should be applied, too: object -> whereUsed() -> lock.

                lock = Lock(lockedObjectClass, locals())
                if lock.isUnlocked():
                    lock.lock()

                    data = {
                        "data": {
                            "items": CustomControllerBase.validate(actionCallback(), Serializer, many=True)
                        },
                        "href": request.get_full_path()
                    }

                    # Check the response's ETag validity (against client request).
                    conditional = Conditional(request)
                    etagCondition = conditional.responseEtagFreshnessAgainstRequest(data["data"])
                    if etagCondition["state"] == "fresh":
                        data = None
                        httpStatus = status.HTTP_304_NOT_MODIFIED
                    else:
                        httpStatus = status.HTTP_200_OK

                    lock.release()
                else:
                    data = None
                    httpStatus = status.HTTP_423_LOCKED
            else:
                data = None
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            Lock(lockedObjectClass, locals()).release()

            data, httpStatus, headers = CustomControllerBase.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(data, status=httpStatus, headers={
            "ETag": etagCondition["responseEtag"],
            "Cache-Control": "must-revalidate"
        })
