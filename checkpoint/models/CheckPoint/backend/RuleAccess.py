from checkpoint.models.CheckPoint.backend.Rule import Rule


class AccessRule(Rule):
    def __init__(self, sessionId: str, assetId: int, domain: str, layerUid: str = "", uid: str = "", *args, **kwargs):
        super().__init__(sessionId, "access", assetId, domain, layerUid, uid, *args, **kwargs)
