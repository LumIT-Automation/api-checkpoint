from typing import List

from checkpoint.models.CheckPoint.backend.Domain import Domain as Backend


class Domain:
    def __init__(self, sessionId: str, assetId: int, name: str = "", uid: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = sessionId
        self.assetId: int = int(assetId)
        self.name: str = name
        self.uid: str = uid



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self) -> dict:
        try:
            return Backend.info(self.sessionId, self.assetId, self.uid)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def listQuick(sessionId: str, assetId: int) -> List[dict]:
        try:
            o = Backend.list(sessionId, assetId)
            o.append({
                "name": "Global" # need to manually append Global domain (oh my!).
            })

            return o
        except Exception as e:
            raise e
