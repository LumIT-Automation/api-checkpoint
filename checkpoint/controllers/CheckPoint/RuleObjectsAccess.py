from checkpoint.controllers.CheckPoint.RuleObjects import CheckPointRuleObjectsController


class CheckPointAccessRuleObjectsController(CheckPointRuleObjectsController):
    def __init__(self, *args, **kwargs):
        super().__init__(ruleType="access", *args, **kwargs)
