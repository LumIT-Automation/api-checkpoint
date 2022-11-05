from checkpoint.controllers.CheckPoint.RuleObjects import CheckPointRuleObjectsController


class CheckPointHttpsRuleObjectsController(CheckPointRuleObjectsController):
    def __init__(self, *args, **kwargs):
        super().__init__(ruleType="https", *args, **kwargs)
