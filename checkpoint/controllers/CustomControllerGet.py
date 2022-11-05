import uuid
from typing import Callable

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from checkpoint.controllers.CustomControllerBase import CustomControllerBase

from checkpoint.helpers.Exception import CustomException
from checkpoint.helpers.Lock import Lock
from checkpoint.helpers.Conditional import Conditional
from checkpoint.helpers.Log import Log


class CustomControllerCheckPointGetInfo(CustomControllerBase):
    def __init__(self, subject: str, *args, **kwargs):
        self.sessionId = uuid.uuid4().hex
        self.subject = subject



    def getInfo(self, request: Request, permission: dict, actionCallback: Callable, assetId: int, objectUid: str, domain: str = "", objectType: str = "", Serializer: Callable = None) -> Response:
        Serializer = Serializer or None

        action = self.subject + "_get" # example: host_get.
        actionLog = f"{self.subject.capitalize()} {objectType} - info {domain} {objectUid}".replace("  ", " ")
        lockedObject = self.subject + objectType # example: host (subject=host) // ruleaccess (subject=rule  + type=access).

        data = dict()
        etagCondition = {"responseEtag": ""}

        try:
            user = CustomControllerBase.loggedUser(request)
            permissionMethod = permission["method"]

            if permissionMethod(groups=user["groups"], action=action, **permission["args"]) or user["authDisabled"]:
                Log.actionLog(actionLog, user)

                # Locking logic for a specific object,
                # example: host:GET:1:POLAND = 'objectUid',
                # example: ruleaccess:GET:1:POLAND = 'objectUid' (when objectType is specified).
                lock = Lock(lockedObject, locals(), objectUid)
                if lock.isUnlocked():
                    lock.lock()

                    data = {
                        "data": self.__validate(actionCallback(), Serializer),
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
            Lock(lockedObject, locals(), locals()["objectUid"]).release()

            data, httpStatus, headers = CustomControllerBase.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(data, status=httpStatus, headers={
            "ETag": etagCondition["responseEtag"],
            "Cache-Control": "must-revalidate"
        })



    def __validate(self, data, Serializer):
        try:
            if Serializer:
                serializer = Serializer(data={"items": data}) # serializer needs an "items" key.
                if serializer.is_valid():
                    return serializer.validated_data["items"]
                else:
                    Log.log("Upstream data incorrect: " + str(serializer.errors))
                    raise CustomException(
                        status=500,
                        payload={"CheckPoint": "upstream data mismatch."}
                    )
            else:
                return data
        except Exception as e:
            raise e



class CustomControllerCheckPointGetList(CustomControllerBase):
    def __init__(self, subject: str, *args, **kwargs):
        self.sessionId = uuid.uuid4().hex
        self.subject = subject



    def getList(self, request: Request, permission: dict, actionCallback: Callable, Serializer: Callable = None, assetId: int = 0, domain: str = "", objectType: str = "", containerObjectUid: str = "") -> Response:
        Serializer = Serializer or None
        data = dict()
        etagCondition = {"responseEtag": ""}

        if self.subject[-1:] == "y":
            action = self.subject[:-1] + "ies_get" # example: categories_get.
        else:
            action = self.subject + "s_get" # example: host_get.
        actionLog = f"{self.subject.capitalize()} {objectType} - list {domain}".replace("  ", " ")
        lockedObject = self.subject + objectType

        try:
            user = CustomControllerBase.loggedUser(request)
            permissionMethod = permission["method"]

            if permissionMethod(groups=user["groups"], action=action, **permission["args"]) or user["authDisabled"]:
                Log.actionLog(actionLog, user)

                # [no containerObjectUid specified] Locking logic for a class of objects, for example: host:GET:1:POLAND = 'any'.
                # [containerObjectUid specified] Locking logic for a specific containerObject, example: hosts within a group: group:GET:1:POLAND = 'containerObjectUid'. # @todo: containerObjectType.
                # A type can also be specified (example: layeraccess:GET:1:POLAND = 'any').
                lock = Lock(lockedObject, locals(), containerObjectUid)
                if lock.isUnlocked():
                    lock.lock()

                    data = {
                        "data": {
                            "items": self.__validate(actionCallback(), Serializer)
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
            Lock(lockedObject, locals(), locals()["containerObjectUid"]).release()

            data, httpStatus, headers = CustomControllerBase.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(data, status=httpStatus, headers={
            "ETag": etagCondition["responseEtag"],
            "Cache-Control": "must-revalidate"
        })



    def __validate(self, data, Serializer):
        try:
            if Serializer:
                serializer = Serializer(data={"items": data}) # serializer needs an "items" key.
                if serializer.is_valid():
                    return serializer.validated_data["items"]
                else:
                    Log.log("Upstream data incorrect: " + str(serializer.errors))
                    raise CustomException(
                        status=500,
                        payload={"CheckPoint": "upstream data mismatch."}
                    )
            else:
                return data
        except Exception as e:
            raise e
