from checkpoint.models.CheckPoint.backend.Rule import Rule


class ThreatRule(Rule):
    def __init__(self, sessionId: str, assetId: int, domain: str, layerUid: str = "", uid: str = "", *args, **kwargs):
        super().__init__(sessionId, "threat", assetId, domain, layerUid, uid, *args, **kwargs)
