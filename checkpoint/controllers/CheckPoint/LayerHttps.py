from checkpoint.controllers.CheckPoint.Layer import CheckPointLayerController


class CheckPointHttpsLayerController(CheckPointLayerController):
    def __init__(self, *args, **kwargs):
        super().__init__(layerType="https", *args, **kwargs)
