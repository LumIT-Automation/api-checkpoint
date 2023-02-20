import ipaddress

from checkpoint.models.CheckPoint.Host import Host
from checkpoint.models.CheckPoint.Rule import Rule
from checkpoint.models.CheckPoint.Network import Network

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
            rolesToIpv4 = list()
            acls = list()

            # Security rules which directly or indirectly reach the host.
            hostsWithIpv4 = Host.searchByIpv4Addresses(self.sessionId, self.assetId, self.domain, self.ipv4Address, localOnly=False)
            if hostsWithIpv4:
                for h in hostsWithIpv4:
                    if "uid" in h and h["uid"]:
                        host = Host(self.sessionId, assetId=self.assetId, domain=self.domain, uid=h["uid"])

                        w = host.whereUsed(indirect=True)
                        for j in ("used-directly", "used-indirectly"):
                            acls.extend(w[j].get("access-control-rules", []))

            # Security rules which reach the network(s) containing the IPv4.
            networks = Network.listQuick(self.sessionId, self.assetId, self.domain, localOnly=False)
            for network in networks:
                if "subnet4" in network and "mask-length4" in network:
                    # If Ipv4 within network.
                    if ipaddress.ip_address(self.ipv4Address) in ipaddress.ip_network(network["subnet4"] + "/" + str(network["mask-length4"])):
                        oNetwork = Network(self.sessionId, self.assetId, self.domain, uid=network["uid"])

                        try:
                            w = oNetwork.whereUsed(indirect=True)
                            for j in ("used-directly", "used-indirectly"):
                                acls.extend(w[j].get("access-control-rules", []))
                        except CustomException as e:
                            if e.status == 404:
                                pass

            # [
            #     {
            #         "rule": {
            #             "uid": "",
            #             "name": "",
            #             "type": "access-rule"
            #         },
            #         "layer": {
            #             "uid": "",
            #             "name": "",
            #             "type": "access-layer"
            #         },
            #         "package": {
            #             "uid": "",
            #             "name": ""
            #         }
            #     },
            #     ...
            # ]

            # Information from collected security rules (if belonging to the package self.package).
            for acl in acls:
                aclInfo = dict()

                if acl.get("package", {}).get("name", "") == self.package:
                    for el in ("rule", "layer"):
                        aclInfo[el] = {
                            "uid": acl.get(str(el), {}).get("uid", ""),
                            "name": acl.get(str(el), {}).get("name", ""),
                        }

                    ruleAcl = Rule(self.sessionId, "access", self.assetId, self.domain, layerUid=aclInfo["layer"]["uid"], uid=aclInfo["rule"]["uid"]).info()

                    # Collect information for all source (active) access roles.
                    if ruleAcl.get("enabled", False):
                        if "source" in ruleAcl:
                            for j in ruleAcl["source"]:
                                if j.get("type", "") == "access-role":
                                    if "uid" in j and "name" in j:
                                        rolesToIpv4.append({
                                            "uid": j["uid"],
                                            "name": j["name"],
                                        })

            # @todo: Network "any".

            return rolesToIpv4
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def usedModels() -> list:
        return ["object", "host", "ruleaccess", "roleaccess"]
