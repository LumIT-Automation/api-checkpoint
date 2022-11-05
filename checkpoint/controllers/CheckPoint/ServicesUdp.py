from checkpoint.controllers.CheckPoint.Services import CheckPointServicesController


class CheckPointServicesUdpController(CheckPointServicesController):
    def __init__(self, *args, **kwargs):
        super().__init__(serviceType="udp", *args, **kwargs)
