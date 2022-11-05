from checkpoint.controllers.CheckPoint.Layers import CheckPointLayersController


class CheckPointAccessLayersController(CheckPointLayersController):
    def __init__(self, *args, **kwargs):
        super().__init__(layerType="access", *args, **kwargs)
