from checkpoint.controllers.CheckPoint.Service import CheckPointServiceController


class CheckPointServiceUdpController(CheckPointServiceController):
    def __init__(self, *args, **kwargs):
        super().__init__(serviceType="udp", *args, **kwargs)
