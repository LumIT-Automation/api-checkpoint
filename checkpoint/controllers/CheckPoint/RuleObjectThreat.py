from checkpoint.controllers.CheckPoint.RuleObject import CheckPointRuleObjectController


class CheckPointThreatRuleObjectController(CheckPointRuleObjectController):
    def __init__(self, *args, **kwargs):
        super().__init__(ruleType="threat", *args, **kwargs)
