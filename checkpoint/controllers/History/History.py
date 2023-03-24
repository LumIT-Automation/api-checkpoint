from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.History.History import History

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetList
from checkpoint.helpers.Log import Log


class HistoryLogsController(CustomControllerCheckPointGetList):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="history", *args, **kwargs)



    def get(self, request: Request) -> Response:
        allUsersHistory = False
        user = CustomControllerCheckPointGetList.loggedUser(request)

        return self.getList(
            request=request,
            actionCallback=lambda: History.list(username=user["username"], allUsersHistory=allUsersHistory),
            permission={
                "args": {}
            }
        )
