from checkpoint.controllers.CheckPoint.RuleObjects import CheckPointRuleObjectsController


class CheckPointThreatRuleObjectsController(CheckPointRuleObjectsController):
    def __init__(self, *args, **kwargs):
        super().__init__(ruleType="threat", *args, **kwargs)
