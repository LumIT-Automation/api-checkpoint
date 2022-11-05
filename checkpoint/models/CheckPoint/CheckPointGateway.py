from typing import List

from checkpoint.models.CheckPoint.backend.CheckPointGateway import CheckPointGateway as Backend


class CheckPointGateway:
    def __init__(self, sessionId: str, assetId: int, uid: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = sessionId
        self.assetId: int = int(assetId)
        self.uid: str = uid



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def listQuick(sessionId: str, assetId: int) -> List[dict]:
        try:
            return Backend.list(sessionId, assetId)
        except Exception as e:
            raise e
