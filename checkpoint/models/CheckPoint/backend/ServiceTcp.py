from checkpoint.models.CheckPoint.backend.Service import Service


class ServiceTcp(Service):
    def __init__(self, sessionId: str, assetId: int, domain: str, uid: str = "", *args, **kwargs):
        super().__init__(sessionId, "tcp", assetId, domain, uid, *args, **kwargs)
