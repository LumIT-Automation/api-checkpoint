from checkpoint.controllers.CheckPoint.Layer import CheckPointLayerController


class CheckPointAccessLayerController(CheckPointLayerController):
    def __init__(self, *args, **kwargs):
        super().__init__(layerType="access", *args, **kwargs)
