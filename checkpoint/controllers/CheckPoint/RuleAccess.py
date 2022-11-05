from checkpoint.controllers.CheckPoint.Rule import CheckPointRuleController


class CheckPointAccessLayerController(CheckPointRuleController):
    def __init__(self, *args, **kwargs):
        super().__init__(ruleType="access", *args, **kwargs)
