from checkpoint.controllers.CheckPoint.RuleObject import CheckPointRuleObjectController


class CheckPointHttpsRuleObjectController(CheckPointRuleObjectController):
    def __init__(self, *args, **kwargs):
        super().__init__(ruleType="https", *args, **kwargs)
