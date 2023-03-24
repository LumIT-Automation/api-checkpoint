from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetInfo
from checkpoint.controllers.CustomControllerPut import CustomControllerCheckPointUpdateAll

from checkpoint.models.Configuration.Configuration import Configuration

from checkpoint.serializers.Configuration.Configuration import ConfigurationSerializer as Serializer


class ConfigurationController(CustomControllerCheckPointGetInfo, CustomControllerCheckPointUpdateAll):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="configuration", *args, **kwargs)



    def get(self, request: Request, configType: str) -> Response:
        return self.getInfo(
            request=request,
            objectUid=str(configType),
            actionCallback=lambda: Configuration(configType=configType).repr(),
            Serializer=Serializer,
            permission={
                "args": {}
            }
        )



    def put(self, request: Request, configType: str) -> Response:
        return self.rewrite(
            request=request,
            assetId=0,
            objectUid=str(configType),
            Serializer=Serializer,
            actionCallback=lambda data: Configuration(configType=configType).rewrite(data),
            permission={
                "args": {}
            }
        )
