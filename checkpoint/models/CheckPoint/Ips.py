from checkpoint.models.CheckPoint.backend.Ips import Ips as Backend


class Ips:
    def __init__(self, sessionId: str, assetId: int, domain: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = sessionId
        self.assetId: int = int(assetId)
        self.domain: str = domain



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self) -> dict:
        try:
            return Backend.info(self.sessionId, self.assetId, self.domain)
        except Exception as e:
            raise e



    def extendedAttributeInfo(self, attributeUid: str) -> dict:
        try:
            return Backend.extendedAttributeInfo(self.sessionId, self.assetId, self.domain, attributeUid=attributeUid)
        except Exception as e:
            raise e



    def runUpdate(self, data: dict = None) -> dict:
        data = data or {}

        try:
            return Backend.runUpdate(self.sessionId, self.assetId, self.domain, data)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def listExtendedAttributes(sessionId: str, assetId: int, domain: str) -> list:
        try:
            return Backend.listExtendedAttributes(sessionId, assetId, domain)
        except Exception as e:
            raise e
