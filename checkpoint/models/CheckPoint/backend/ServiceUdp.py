from checkpoint.models.CheckPoint.backend.Service import Service


class ServiceUdp(Service):
    def __init__(self, sessionId: str, assetId: int, domain: str, uid: str = "", *args, **kwargs):
        super().__init__(sessionId, "udp", assetId, domain, uid, *args, **kwargs)
