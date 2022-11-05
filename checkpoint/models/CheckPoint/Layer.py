from typing import List


class LayerBackendFactory:
    def __init__(self, layerType):
        self.layerType = layerType

    def __call__(self, *args, **kwargs):
        try:
            if self.layerType == "access":
                from checkpoint.models.CheckPoint.backend.LayerAccess import AccessLayer as Backend
            elif self.layerType == "threat":
                from checkpoint.models.CheckPoint.backend.LayerThreat import ThreatLayer as Backend
            elif self.layerType == "https":
                from checkpoint.models.CheckPoint.backend.LayerHttps import HttpsLayer as Backend
            else:
                raise NotImplementedError

            return Backend
        except Exception as e:
            raise e



class Layer:
    def __init__(self, sessionId: str, layerType: str, assetId: int, domain: str, uid: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = sessionId
        self.type: str = layerType
        self.assetId: int = int(assetId)
        self.domain: str = domain
        self.uid: str = uid

        self.Backend = LayerBackendFactory(layerType)() # get suitable Backend.



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self) -> dict:
        try:
            return self.Backend(self.sessionId, self.assetId, self.domain, self.uid).info()
        except Exception as e:
            raise e



    def modify(self, data: dict, autoPublish: bool = True) -> None:
        try:
            self.Backend(self.sessionId, self.assetId, self.domain, self.uid).modify(data, autoPublish)
        except Exception as e:
            raise e



    def delete(self, autoPublish: bool = True) -> None:
        try:
            self.Backend(self.sessionId, self.assetId, self.domain, self.uid).delete(autoPublish)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def listQuick(sessionId: str, layerType: str, assetId: int, domain: str, localOnly: bool = False) -> List[dict]:
        out = list()

        try:
            Backend = LayerBackendFactory(layerType)() # get suitable Backend.
            if localOnly:
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
    def add(sessionId: str, layerType: str, assetId: int, domain: str, data: dict, autoPublish: bool = True) -> dict:
        out = dict()

        try:
            Backend = LayerBackendFactory(layerType)() # get suitable Backend.
            o = Backend(sessionId, assetId, domain).add(data, autoPublish)

            out["uid"] = o.get("uid", "")
        except Exception as e:
            raise e

        return out



    @staticmethod
    def listRules(sessionId: str, layerType: str, assetId: int, domain: str, accessLayerUid: str, localOnly: bool = False) -> List[dict]:
        out = list()

        try:
            Backend = LayerBackendFactory(layerType)()
            if localOnly:
                l = Backend(sessionId, assetId, domain, accessLayerUid).listRules()
                for el in l:
                    if "rulebase" in el:
                        for elm in el["rulebase"]:
                            if "domain" in elm and "domain-type" in elm["domain"]:
                                if elm["domain"]["domain-type"] != "global domain":
                                    out.append(el)
            else:
                out = Backend(sessionId, assetId, domain, accessLayerUid).listRules()
        except Exception as e:
            raise e

        return out
