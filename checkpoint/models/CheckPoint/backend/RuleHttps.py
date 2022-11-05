from checkpoint.models.CheckPoint.backend.Rule import Rule


class HttpsRule(Rule):
    def __init__(self, sessionId: str, assetId: int, domain: str, layerUid: str = "", uid: str = "", *args, **kwargs):
        super().__init__(sessionId, "https", assetId, domain, layerUid, uid, *args, **kwargs)
