from checkpoint.models.CheckPoint.Host import Host
from checkpoint.models.CheckPoint.Rule import Rule

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

    def __call__(self, *args, **kwargs) -> list:
        try:
            aclInformation = list()

            # Find where the host is used within the domain.
            # More than one host can coexist with the same IPv4 address, but with different names.
            hostsWithIpv4 = Host.searchByIpv4Addresses(self.sessionId, self.assetId, self.domain, self.ipv4Address, localOnly=False)
            for h in hostsWithIpv4:
                if h:
                    hostUid = h["uid"]
                    host = Host(self.sessionId, assetId=self.assetId, domain=self.domain, uid=hostUid)

                    w = host.whereUsed()
                    if "used-directly" in w:
                        for hostAcl in w["used-directly"].get("access-control-rules", []):
                            hostAclInformation = dict()

                            # Access control rule information.
                            for el in ("rule", "layer"):
                                hostAclInformation[el] = {
                                    "uid": hostAcl.get(str(el), {}).get("uid", ""),
                                    "name": hostAcl.get(str(el), {}).get("name", ""),
                                }

                            acl = Rule(self.sessionId, "access", self.assetId, self.domain, layerUid=hostAclInformation["layer"]["uid"], uid=hostAclInformation["rule"]["uid"]).info()
                            if "source" in acl:
                                for j in acl["source"]:
                                    aclInformation.append({
                                        "uid": j.get("uid", ""),
                                        "name": j.get("name", ""),
                                    })

            return aclInformation
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def usedModels() -> list:
        return ["object", "host", "ruleaccess", "roleaccess"]



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    # def __log(self, domain: str, message: str, object_type: str, object: str, status: str) -> None:
    #     try:
    #         Log.log(f"[WORKFLOW {self.workflowId}] [Domain: {domain}] [Username: {self.username}] " + str(message), "_")
    #     except Exception:
    #         pass
