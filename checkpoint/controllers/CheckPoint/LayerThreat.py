from checkpoint.controllers.CheckPoint.Layer import CheckPointLayerController


class CheckPointThreatLayerController(CheckPointLayerController):
    def __init__(self, *args, **kwargs):
        super().__init__(layerType="threat", *args, **kwargs)
