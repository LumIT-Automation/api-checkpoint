from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from checkpoint.models.History import History
from checkpoint.models.Permission.Permission import Permission

from checkpoint.serializers.History import HistorySerializer as Serializer

from checkpoint.controllers.CustomControllerBase import CustomControllerBase
from checkpoint.helpers.Conditional import Conditional
from checkpoint.helpers.Log import Log


class HistoryLogsController(CustomControllerBase):
    @staticmethod
    def get(request: Request) -> Response:
        allUsersHistory = False
        data = dict()

        user = CustomControllerBase.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="historyComplete_get") or user["authDisabled"]:
                allUsersHistory = True

            Log.actionLog("History log", user)

            itemData = History.list(user["username"], allUsersHistory)
            data["data"] = Serializer(itemData).data["data"]
            data["href"] = request.get_full_path()

            # Check the response's ETag validity (against client request).
            conditional = Conditional(request)
            etagCondition = conditional.responseEtagFreshnessAgainstRequest(data["data"])
            if etagCondition["state"] == "fresh":
                data = None
                httpStatus = status.HTTP_304_NOT_MODIFIED
            else:
                httpStatus = status.HTTP_200_OK

        except Exception as e:
            data, httpStatus, headers = CustomControllerBase.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(data, status=httpStatus, headers={
            "ETag": etagCondition["responseEtag"],
            "Cache-Control": "must-revalidate"
        })
