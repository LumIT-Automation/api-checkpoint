from typing import List

from checkpoint.models.CheckPoint.Domain import Domain
from checkpoint.models.CheckPoint.Host import Host
from checkpoint.models.CheckPoint.Group import Group
from checkpoint.models.CheckPoint.GroupHost import GroupHost
from checkpoint.models.CheckPoint.RuleObject import RuleObject
from checkpoint.models.CheckPoint.Rule import Rule
from checkpoint.models.CheckPoint.NatRule import NatRule
from checkpoint.models.CheckPoint.Session import Session
from checkpoint.models.History.History import History

from checkpoint.helpers.Exception import CustomException
from checkpoint.helpers.Log import Log


class VpnToHost:
    def __init__(self, sessionId: str, assetId: int, domain: str, ipv4Address: str, user: str, workflowId: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = sessionId
        self.assetId: int = int(assetId)
        self.domain: str = domain
        self.username = user
        self.workflowId = workflowId
        self.ipv4Address: str = ipv4Address



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def __call__(self, *args, **kwargs) -> None:
        pass



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def usedModels() -> list:
        return ["object", "host", "group", "rule_access", "rule_threat", "rule_https", "nat_rule"]



    ####################################################################################################################
    # Private methods
    ####################################################################################################################


    # def __log(self, domain: str, message: str, object_type: str, object: str, status: str) -> None:
    #     try:
    #         Log.log(f"[WORKFLOW {self.workflowId}] [Domain: {domain}] [Username: {self.username}] " + str(message), "_")
    #     except Exception:
    #         pass
    #
    #     try:
    #         History.add({
    #             "username": self.username,
    #             "action": message,
    #             "asset_id": self.assetId,
    #             "workflow_id": self.workflowId,
    #             "config_object_type": object_type,
    #             "config_object": object,
    #             "domain": domain,
    #             "status": status
    #         })
    #     except Exception:
    #         pass
