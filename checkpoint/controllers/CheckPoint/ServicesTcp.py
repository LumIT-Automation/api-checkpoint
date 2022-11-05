from checkpoint.controllers.CheckPoint.Services import CheckPointServicesController


class CheckPointServicesTcpController(CheckPointServicesController):
    def __init__(self, *args, **kwargs):
        super().__init__(serviceType="tcp", *args, **kwargs)
