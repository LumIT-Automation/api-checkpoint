from checkpoint.controllers.CheckPoint.Rulebase import CheckPointRulebaseController


class CheckPointThreatRulebaseController(CheckPointRulebaseController):
    def __init__(self, *args, **kwargs):
        super().__init__(layerType="threat", *args, **kwargs)
