import uuid
import time

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from checkpoint.models.CheckPoint.Group import Group
from checkpoint.models.CheckPoint.Session import Session
from checkpoint.models.Permission.Permission import Permission

from checkpoint.serializers.CheckPoint.GroupGroups import CheckPointGroupGroupsSerializer as Serializer

from checkpoint.controllers.CustomControllerBase import CustomControllerBase

from checkpoint.helpers.Lock import Lock
from checkpoint.helpers.Conditional import Conditional
from checkpoint.helpers.Log import Log


class CheckPointGroupGroupsController(CustomControllerBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = uuid.uuid4().hex



    def get(self, request: Request, assetId: int, domain: str, groupUid: str) -> Response:
        data = dict()
        itemData = dict()
        etagCondition = {"responseEtag": ""}
        user = CustomControllerBase.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="group_get", assetId=assetId) or user["authDisabled"]:
                Log.actionLog("Group hosts info: domain: "+str(domain)+" uid: "+str(groupUid), user)

                lock = Lock("group", locals(), groupUid)
                if lock.isUnlocked():
                    lock.lock()

                    data = {
                        "data": {
                            "items": Group(sessionId="", assetId=assetId, domain=domain, uid=groupUid).listInnerGroups()
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
            Lock("group", locals(), locals()["groupUid"]).release()

            data, httpStatus, headers = CustomControllerBase.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(data, status=httpStatus, headers={
            "ETag": etagCondition["responseEtag"],
            "Cache-Control": "must-revalidate"
        })



    def post(self, request: Request, assetId: int, domain: str, groupUid: str) -> Response:
        response = None
        user = CustomControllerBase.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="groups_post", assetId=assetId) or user["authDisabled"]:
                Log.actionLog("Group group addition", user)
                Log.actionLog("User data: "+str(request.data), user)

                serializer = Serializer(data=request.data)
                if serializer.is_valid():
                    data = serializer.validated_data["data"]
                    lock = Lock("group", locals(), groupUid)
                    if lock.isUnlocked():
                        lock.lock()

                        Group(sessionId=self.sessionId, assetId=assetId, domain=domain, uid=groupUid).addInnerGroup(data["groups"])
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

                    Log.actionLog("User data incorrect: "+str(response), user)
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

        return Response(response, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
