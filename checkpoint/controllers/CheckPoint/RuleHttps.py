from checkpoint.controllers.CheckPoint.Rule import CheckPointRuleController


class CheckPointHttpsLayerController(CheckPointRuleController):
    def __init__(self, *args, **kwargs):
        super().__init__(ruleType="https", *args, **kwargs)
