from checkpoint.models.CheckPoint.backend.Ips import Ips as Backend


class IpsSchedule():
    def __init__(self, sessionId: str, assetId: int, domain: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = sessionId
        self.assetId: int = int(assetId)
        self.domain: str = domain



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self) -> dict:
        try:
            return Backend.updateScheduleInfo(self.sessionId, self.assetId, self.domain)
        except Exception as e:
            raise e



    def modify(self, data: dict) -> dict:
        try:
            return Backend.updateScheduleModify(self.sessionId, self.assetId, self.domain, data)
        except Exception as e:
            raise e
