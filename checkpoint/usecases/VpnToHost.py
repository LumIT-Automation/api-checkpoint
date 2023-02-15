from checkpoint.models.CheckPoint.Host import Host
from checkpoint.models.CheckPoint.Rule import Rule

from checkpoint.helpers.Exception import CustomException
from checkpoint.helpers.Log import Log


class VpnToHost:
    def __init__(self, sessionId: str, assetId: int, domain: str, package: str, ipv4Address: str, user: str, workflowId: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = sessionId
        self.assetId: int = int(assetId)
        self.domain: str = domain
        self.package: str = package
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

            if hostsWithIpv4:
                for h in hostsWithIpv4:
                    if h and "uid" in h:
                        hostUid = h["uid"]
                        host = Host(self.sessionId, assetId=self.assetId, domain=self.domain, uid=hostUid)

                        w = host.whereUsed(indirect=True)
                        hostAcls = list()

                        if "used-directly" in w:
                            hostAcls.extend(w["used-directly"].get("access-control-rules", []))

                        if "used-indirectly" in w:
                            hostAcls.extend(w["used-indirectly"].get("access-control-rules", []))

                        for hostAcl in hostAcls:
                            hostAclInformation = dict()

                            # Access control rule information.
                            if hostAcl.get("package", {}).get("name", "") == self.package:
                                for el in ("rule", "layer"):
                                    hostAclInformation[el] = {
                                        "uid": hostAcl.get(str(el), {}).get("uid", ""),
                                        "name": hostAcl.get(str(el), {}).get("name", ""),
                                    }

                                acl = Rule(self.sessionId, "access", self.assetId, self.domain, layerUid=hostAclInformation["layer"]["uid"], uid=hostAclInformation["rule"]["uid"]).info()
                                if "source" in acl:
                                    for j in acl["source"]:
                                        if j.get("type", "") == "access-role":
                                            aclInformation.append({
                                                "uid": j.get("uid", ""),
                                                "name": j.get("name", ""),
                                            })
            else:
                raise CustomException(status=404, payload={"CheckPoint": "host not found"})

            return aclInformation
        except Exception as e:
            raise e


    # @todo:
    # List networks for domain <DOMAIN> (Globals, too)
    #   "subnet4": "202.164.210.0",
    #   "mask-length4": 24,
    #   "subnet-mask": "255.255.255.0",
    # WHICH ONE CONTAINS THE IPv4?
    # -> where used

    # Network "any" ??



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def usedModels() -> list:
        return ["object", "host", "ruleaccess", "roleaccess"]
