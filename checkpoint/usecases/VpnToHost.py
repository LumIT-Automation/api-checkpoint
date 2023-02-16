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
            aclInformation = list()

            hostsWithIpv4 = Host.searchByIpv4Addresses(self.sessionId, self.assetId, self.domain, self.ipv4Address, localOnly=False)
            if hostsWithIpv4:
                for h in hostsWithIpv4:
                    if h and "uid" in h:
                        hostUid = h["uid"]
                        host = Host(self.sessionId, assetId=self.assetId, domain=self.domain, uid=hostUid)

                        # Security rules (and related roles) which directly or indirectly reach the host.
                        # Find where the host is used within the domain.       
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

            # Security rules (and related roles) which reach the network(s) containing the IPv4.
            networks = Network.listQuick(self.sessionId, self.assetId, self.domain, localOnly=False)
            for network in networks:
                if "subnet4" in network and "mask-length4" in network:
                    # If Ipv4 within network.
                    if ipaddress.ip_address(self.ipv4Address) in ipaddress.ip_network(network["subnet4"] + "/" + str(network["mask-length4"])):
                        oNetwork = Network(self.sessionId, self.assetId, self.domain, uid=network["uid"])

                        try:
                            w = oNetwork.whereUsed(indirect=True)
                            networkAcls = list()

                            if "used-directly" in w:
                                networkAcls.extend(w["used-directly"].get("access-control-rules", []))

                            if "used-indirectly" in w:
                                networkAcls.extend(w["used-indirectly"].get("access-control-rules", []))

                            for networkAcl in networkAcls:
                                networkAclInformation = dict()

                                # Access control rule information.
                                if networkAcl.get("package", {}).get("name", "") == self.package:
                                    for el in ("rule", "layer"):
                                        networkAclInformation[el] = {
                                            "uid": networkAcl.get(str(el), {}).get("uid", ""),
                                            "name": networkAcl.get(str(el), {}).get("name", ""),
                                        }

                                    acl = Rule(self.sessionId, "access", self.assetId, self.domain, layerUid=networkAclInformation["layer"]["uid"], uid=networkAclInformation["rule"]["uid"]).info()
                                    if "source" in acl:
                                        for j in acl["source"]:
                                            if j.get("type", "") == "access-role":
                                                aclInformation.append({
                                                    "uid": j.get("uid", ""),
                                                    "name": j.get("name", ""),
                                                })
                        except CustomException as e:
                            if e.status == 404:
                                pass

            # @todo: Network "any".

            return aclInformation
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def usedModels() -> list:
        return ["object", "host", "ruleaccess", "roleaccess"]
