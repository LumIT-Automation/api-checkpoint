from rest_framework.request import Request
from rest_framework.response import Response

from checkpoint.models.CheckPoint.Service import Service
from checkpoint.models.Permission.Permission import Permission

from checkpoint.controllers.CustomControllerGet import CustomControllerCheckPointGetList
from checkpoint.controllers.CustomControllerPost import CustomControllerCheckPointCreate


class ServiceControllerFactory:
    def __init__(self, serviceType):
        self.serviceType = serviceType

    def __call__(self, *args, **kwargs):
        try:
            if self.serviceType == "tcp":
                from checkpoint.serializers.CheckPoint.ServiceTcp import CheckPointServiceTcpSerializer as Serializer
            elif self.serviceType == "udp":
                from checkpoint.serializers.CheckPoint.ServiceUdp import CheckPointServiceUdpSerializer as Serializer
            else:
                raise NotImplementedError

            return Serializer
        except Exception as e:
            raise e



class CheckPointServicesController(CustomControllerCheckPointGetList, CustomControllerCheckPointCreate):
    def __init__(self, serviceType: str, *args, **kwargs):
        super().__init__(subject="service", *args, **kwargs)

        self.serviceType = serviceType



    def get(self, request: Request, assetId: int, domain: str) -> Response:
        def actionCallback():
            localOnly = False
            if "local" in request.GET:
                localOnly = True

            return Service.listQuick(sessionId="", serviceType=self.serviceType, assetId=assetId, domain=domain, localOnly=localOnly)

        return self.getList(
            request=request,
            assetId=assetId,
            domain=domain,
            objectType=self.serviceType,
            actionCallback=actionCallback,
            permission={
                "method": Permission.hasUserPermission,
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )



    def post(self, request: Request, assetId: int, domain: str) -> Response:
        def actionCallback(data):
            return Service.add(sessionId=self.sessionId, serviceType=self.serviceType, assetId=assetId, domain=domain, data=data)

        return self.create(
            request=request,
            assetId=assetId,
            domain=domain,
            objectType=self.serviceType,
            Serializer=ServiceControllerFactory(self.serviceType)(), # get suitable Serializer.
            actionCallback=actionCallback,
            permission={
                "method": Permission.hasUserPermission,
                "args": {
                    "assetId": assetId,
                    "domain": domain
                }
            }
        )
