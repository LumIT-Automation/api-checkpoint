from typing import List

from checkpoint.helpers.Lang import Lang


class ServiceBackendFactory:
    def __init__(self, serviceType):
        self.serviceType = serviceType

    def __call__(self, *args, **kwargs):
        try:
            if self.serviceType == "tcp":
                from checkpoint.models.CheckPoint.backend.ServiceTcp import ServiceTcp as Backend
            elif self.serviceType == "udp":
                from checkpoint.models.CheckPoint.backend.ServiceUdp import ServiceUdp as Backend
            else:
                raise NotImplementedError

            return Backend
        except Exception as e:
            raise e



class Service:
    def __init__(self, sessionId: str, serviceType: str, assetId: int, domain: str = "", name: str = "", uid: str = "", port: int = None, protocol: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = sessionId
        self.assetId: int = int(assetId)
        self.domain: str = domain
        self.name: str = name
        self.uid: str = uid
        self.port: int = port
        self.protocol: str = protocol

        self.Backend = ServiceBackendFactory(serviceType)() # get suitable Backend.



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self) -> dict:
        try:
            o = self.Backend(self.sessionId, self.assetId, self.domain, self.uid).info()

            # Cleanup redundant data.
            if "groups" in o:
                for group in o["groups"]:
                    if "members" in group:
                        del group["members"]
            return o
        except Exception as e:
            raise e



    def modify(self, data: dict, autoPublish: bool = True) -> None:
        try:
            self.Backend(self.sessionId, self.assetId, self.domain, self.uid).modify(data, autoPublish)

            for k, v in Lang.toDict(data).items():
                setattr(self, k, v)
        except Exception as e:
            raise e
 


    def delete(self, autoPublish: bool = True) -> None:
        try:
            self.Backend(self.sessionId, self.assetId, self.domain, self.uid).delete(autoPublish)
            del self
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def listQuick(sessionId: str, serviceType: str, assetId: int, domain: str, localOnly: bool = False) -> List[dict]:
        out = list()

        try:
            Backend = ServiceBackendFactory(serviceType)() # get suitable Backend.

            if localOnly and domain != "Global":
                o = Backend(sessionId, assetId, domain).list()
                for el in o:
                    if "domain" in el and "domain-type" in el["domain"]:
                        if el["domain"]["domain-type"] != "global domain":
                            out.append(el)
            else:
                out = Backend(sessionId, assetId, domain).list()
        except Exception as e:
            raise e

        return out



    @staticmethod
    def add(sessionId: str, serviceType: str, assetId: int, domain: str, data: dict, autoPublish: bool = True) -> dict:
        out = dict()

        try:
            Backend = ServiceBackendFactory(serviceType)() # get suitable Backend.
            o = Backend(sessionId, assetId, domain).add(data, autoPublish)

            out["uid"] = o.get("uid", "")
        except Exception as e:
            raise e

        return out
 