import uuid
import time

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from checkpoint.models.CheckPoint.PolicyPackage import PolicyPackage
from checkpoint.models.CheckPoint.Session import Session
from checkpoint.models.Permission.Permission import Permission

from checkpoint.controllers.CustomControllerBase import CustomControllerBase

from checkpoint.serializers.CheckPoint.NatRuleBase import CheckPointNatRuleBaseSerializer as Serializer

from checkpoint.helpers.Lock import Lock
from checkpoint.helpers.Conditional import Conditional
from checkpoint.helpers.Log import Log


class CheckPointNatRulebaseController(CustomControllerBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = uuid.uuid4().hex



    def get(self, request: Request, assetId: int, domain: str, packageUid: str) -> Response:
        data = dict()
        etagCondition = {"responseEtag": ""}
        user = CustomControllerBase.loggedUser(request)

        localOnly = False
        if "local" in request.GET:
            localOnly = True

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="nat_rulebase_get", assetId=assetId, domain=domain) or user["authDisabled"]:
                Log.actionLog("NAT rulebases list", user)

                lock = Lock("nat_rulebase", locals())
                if lock.isUnlocked():
                    lock.lock()

                    data = {
                        "data": {
                            "items": PolicyPackage.listNatRules(sessionId="", assetId=assetId, domain=domain, policyPackageUid=packageUid, localOnly=localOnly)
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
            Lock("nat_rulebase", locals()).release()

            data, httpStatus, headers = CustomControllerBase.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(data, status=httpStatus, headers={
            "ETag": etagCondition["responseEtag"],
            "Cache-Control": "must-revalidate"
        })



    def post(self, request: Request, assetId: int, domain: str, packageUid: str) -> Response:
        response = dict()
        user = CustomControllerBase.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="nat_rulebase_post", assetId=assetId, domain=domain) or user["authDisabled"]:
                Log.actionLog("NAT rule addition", user)
                Log.actionLog("User data: "+str(request.data), user)

                serializer = Serializer(data=request.data["data"], partial=True)
                if serializer.is_valid():
                    data = serializer.validated_data

                    lock = Lock("nat_rule", locals())
                    if lock.isUnlocked():
                        lock.lock()

                        response["data"] = PolicyPackage.addNatRule(sessionId=self.sessionId, assetId=assetId, domain=domain, policyPackageUid=packageUid, data=data)
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
            Lock("nat_rule", locals()).release()

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
