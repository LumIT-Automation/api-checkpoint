import uuid
import time

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from checkpoint.models.Permission.Permission import Permission
from checkpoint.models.CheckPoint.Session import Session

from checkpoint.usecases.VpnToServices import VpnToServices

from checkpoint.serializers.CheckPoint.UseCases.VpnToServices import CheckPointVpnToServicesSerializer as Serializer
from checkpoint.controllers.CustomControllerBase import CustomControllerBase

from checkpoint.helpers.Lock import Lock
from checkpoint.helpers.Misc import Misc
from checkpoint.helpers.Log import Log


class CheckPointVpnProfileToServicesController(CustomControllerBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = uuid.uuid4().hex



    def put(self, request: Request, assetId: int, domain: str) -> Response:
        response = {"data": dict()}
        httpStatus = status.HTTP_500_INTERNAL_SERVER_ERROR
        user = CustomControllerBase.loggedUser(request)

        originalUsername = request.headers.get("workflowUser", "") # user who called the workflow, if any.
        workflowId = request.headers.get("workflowId", "") # a correlation id.

        # Direct requests to the api container should be logged, too.
        if not originalUsername:
            originalUsername = user.get("username", "")
        if not workflowId:
            workflowId = 'api-vpn_to_profiles-' + Misc.getWorkflowCorrelationId()

        try:
            Log.actionLog("Services reached by the VPN profile", user)
            if originalUsername:
                Log.actionLog("[Original user for VPN to services]", {"username": originalUsername})
            if workflowId:
                Log.actionLog("[Workflow id for VPN to services: " + workflowId, {"username": originalUsername})

            if Permission.hasUserPermission(groups=user["groups"], action="vpn_to_services", assetId=assetId) or user["authDisabled"]:
                serializer = Serializer(data=request.data.get("data", {}))
                if serializer.is_valid():
                    data = serializer.validated_data

                    lockUseCase = Lock("vpn_to_services", locals(), data["name"])
                    lock = Lock(VpnToServices.usedModels(), locals())
                    if lockUseCase.isUnlocked() and lock.isUnlocked():
                        lockUseCase.lock()
                        lock.lock()

                        response["data"]["items"] = VpnToServices(sessionId=self.sessionId, assetId=assetId, domain=domain, name=data["name"], user=originalUsername, workflowId=workflowId)()
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
                    Log.actionLog("User data incorrect: " + str(response), user)
            else:
                response = None
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            if "serializer" in locals():
                Lock("vpn_to_services", locals(), locals()["serializer"].data["name"]).release()
            Lock(VpnToServices.usedModels(), locals()).release()

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
