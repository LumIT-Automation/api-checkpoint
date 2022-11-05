from checkpoint.controllers.CheckPoint.Layers import CheckPointLayersController


class CheckPointHttpsLayersController(CheckPointLayersController):
    def __init__(self, *args, **kwargs):
        super().__init__(layerType="https", *args, **kwargs)
