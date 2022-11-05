from checkpoint.controllers.CheckPoint.Rulebase import CheckPointRulebaseController


class CheckPointAccessRulebaseController(CheckPointRulebaseController):
    def __init__(self, *args, **kwargs):
        super().__init__(layerType="access", *args, **kwargs)
