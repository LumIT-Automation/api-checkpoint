from checkpoint.controllers.CheckPoint.Rulebase import CheckPointRulebaseController


class CheckPointHttpsRulebaseController(CheckPointRulebaseController):
    def __init__(self, *args, **kwargs):
        super().__init__(layerType="https", *args, **kwargs)
