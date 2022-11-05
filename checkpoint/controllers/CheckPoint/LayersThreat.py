from checkpoint.controllers.CheckPoint.Layers import CheckPointLayersController


class CheckPointThreatLayersController(CheckPointLayersController):
    def __init__(self, *args, **kwargs):
        super().__init__(layerType="threat", *args, **kwargs)
