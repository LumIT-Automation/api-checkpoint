from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.Permission.Permission import Permission

from checkpoint.controllers.CustomControllerBase import CustomControllerBase
from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetList


class AuthorizationsController(CustomControllerCheckPointGetList):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="authorization", *args, **kwargs)



    def get(self, request: Request) -> Response:
        user = CustomControllerBase.loggedUser(request)

        return self.getList(
            request=request,
            actionCallback=lambda: Permission.authorizationsList(user["groups"]),
            permission={
                "args": {
                }
            }
        )
