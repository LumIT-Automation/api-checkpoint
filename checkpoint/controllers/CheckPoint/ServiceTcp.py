from checkpoint.controllers.CheckPoint.Service import CheckPointServiceController


class CheckPointServiceTcpController(CheckPointServiceController):
    def __init__(self, *args, **kwargs):
        super().__init__(serviceType="tcp", *args, **kwargs)
