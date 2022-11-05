from checkpoint.models.CheckPoint.backend.Layer import Layer


class ThreatLayer(Layer):
    def __init__(self, sessionId: str, assetId: int, domain: str, uid: str = "", *args, **kwargs):
        super().__init__(sessionId, "threat", assetId, domain, uid, *args, **kwargs)
