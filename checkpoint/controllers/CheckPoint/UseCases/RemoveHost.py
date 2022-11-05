import uuid
import time

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from checkpoint.models.CheckPoint.Domain import Domain
from checkpoint.models.Permission.Permission import Permission
from checkpoint.models.CheckPoint.Session import Session

from checkpoint.usecases.HostRemoval import HostRemoval

from checkpoint.serializers.CheckPoint.UseCases.RemoveHost import CheckPointRemoveHostSerializer as Serializer
from checkpoint.controllers.CustomControllerBase import CustomControllerBase

from checkpoint.helpers.Lock import Lock
from checkpoint.helpers.Log import Log


class CheckPointRemoveHostController(CustomControllerBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = uuid.uuid4().hex



    def put(self, request: Request, assetId: int) -> Response:
        response = None
        httpStatus = status.HTTP_500_INTERNAL_SERVER_ERROR
        user = CustomControllerBase.loggedUser(request)
        originalUsername = request.headers.get("workflowUser", "") # user who called the workflow, if any.
        workflowId = request.headers.get("workflowId", "") # a correlation id.

        try:
            Log.actionLog("Host complete removal", user)
            if originalUsername:
                Log.actionLog("[Original user for Host complete removal]", {"username": originalUsername})
            if workflowId:
                Log.actionLog("[Workflow id for Host complete removal: "+workflowId, {"username": originalUsername})

            if Permission.hasUserPermission(groups=user["groups"], action="host_remove", assetId=assetId) or user["authDisabled"]:
                serializer = Serializer(data=request.data["data"])
                if serializer.is_valid():
                    data = serializer.validated_data

                    lockUseCase = Lock("remove_host", locals(), data["ipv4-address"])
                    lock = Lock(HostRemoval.usedModels(), locals())
                    if lockUseCase.isUnlocked() and lock.isUnlocked():
                        lockUseCase.lock()
                        lock.lock()

                        HostRemoval(sessionId=self.sessionId, assetId=assetId, ipv4Address=data["ipv4-address"])()
                        httpStatus = status.HTTP_200_OK

                        lockUseCase.release()
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
            if "serializer" in locals():
                Lock("remove_host", locals(), locals()["serializer"].data["ipv4-address"]).release()
            Lock(HostRemoval.usedModels(), locals()).release()

            data, httpStatus, headers = CustomControllerBase.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)
        finally:
            try:
                if httpStatus != status.HTTP_423_LOCKED and httpStatus != status.HTTP_400_BAD_REQUEST and httpStatus != status.HTTP_403_FORBIDDEN:
                    domains = Domain.listQuick(self.sessionId, assetId)

                    for domain in domains:
                        Session(sessionId=self.sessionId, assetId=assetId, domain=domain["name"]).logout()
                        time.sleep(0.5) # avoid "Too many requests" error.
            except Exception:
                pass

        return Response(response, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
