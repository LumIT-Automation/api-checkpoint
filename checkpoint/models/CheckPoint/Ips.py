from checkpoint.models.CheckPoint.backend.Ips import Ips as Backend


class Ips():
    def __init__(self, sessionId: str, assetId: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = sessionId
        self.assetId: int = int(assetId)



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self) -> dict:
        try:
            return Backend.info(self.sessionId, self.assetId)
        except Exception as e:
            raise e



    def runUpdate(self, data: dict = None) -> dict:
        data = data or {}

        try:
            return Backend.runUpdate(self.sessionId, self.assetId, data)
        except Exception as e:
            raise e