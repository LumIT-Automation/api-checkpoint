from checkpoint.controllers.CheckPoint.Rule import CheckPointRuleController


class CheckPointThreatLayerController(CheckPointRuleController):
    def __init__(self, *args, **kwargs):
        super().__init__(ruleType="threat", *args, **kwargs)
