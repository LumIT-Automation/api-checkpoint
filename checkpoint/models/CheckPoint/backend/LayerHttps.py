from checkpoint.models.CheckPoint.backend.Layer import Layer


class HttpsLayer(Layer):
    def __init__(self, sessionId: str, assetId: int, domain: str, uid: str = "", *args, **kwargs):
        super().__init__(sessionId, "https", assetId, domain, uid, *args, **kwargs)
