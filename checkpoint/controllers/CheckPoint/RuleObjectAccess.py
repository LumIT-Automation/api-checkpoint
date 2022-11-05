from checkpoint.controllers.CheckPoint.RuleObject import CheckPointRuleObjectController


class CheckPointAccessRuleObjectController(CheckPointRuleObjectController):
    def __init__(self, *args, **kwargs):
        super().__init__(ruleType="access", *args, **kwargs)
