from checkpoint.models.CheckPoint.backend.Layer import Layer


class AccessLayer(Layer):
    def __init__(self, sessionId: str, assetId: int, domain: str, uid: str = "", *args, **kwargs):
        super().__init__(sessionId, "access", assetId, domain, uid, *args, **kwargs)
