import ipaddress

from checkpoint.models.CheckPoint.Host import Host
from checkpoint.models.CheckPoint.Layer import Layer
from checkpoint.models.CheckPoint.Rule import Rule
from checkpoint.models.CheckPoint.Role import Role
from checkpoint.models.CheckPoint.Network import Network
from checkpoint.models.CheckPoint.AddressRange import AddressRange

from checkpoint.helpers.Exception import CustomException
from checkpoint.helpers.Network import Network as NetworkHelper
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
            no = 0
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

            # Security rules which reach the address range(s) containing the IPv4.
            ranges = AddressRange.listQuick(self.sessionId, self.assetId, self.domain, localOnly=False)
            for r in ranges:
                if "ipv4-address-first" in r and "ipv4-address-last" in r:
                    # If Ipv4 within address range.
                    if NetworkHelper.ipv4InRange(self.ipv4Address, r["ipv4-address-first"], r["ipv4-address-last"]):
                        oAddressRange = AddressRange(self.sessionId, self.assetId, domain=self.domain, uid=r["uid"])

                        try:
                            w = oAddressRange.whereUsed(indirect=True)
                            for j in ("used-directly", "used-indirectly"):
                                acls.extend(w[j].get("access-control-rules", []))
                        except CustomException as e:
                            if e.status == 404:
                                pass

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
                                        if "NETWORK_LOCAL" not in j["name"]:
                                            rolesToIpv4.append({
                                                j["uid"]: {
                                                    "name": j["name"]
                                                }
                                            })

                                            if "service" in ruleAcl:
                                                for s in ruleAcl["service"]:
                                                    if "port" in s and "protocol" in s:
                                                        rolesToIpv4[no].update({
                                                            "port": s["port"],
                                                            "protocol": s["protocol"],
                                                        })
                                                    if "type" in s:
                                                        rolesToIpv4[no].update({"type": s["type"]})

                                            no += 1

            # Alternative approach.
            # Find all access control rules with self.ipv4Address as destination.
            # layers = Layer.listQuick(sessionId=self.sessionId, layerType="access", assetId=self.assetId, domain=self.domain)
            # for l in layers:
            #     acls.extend(Layer.listRules(sessionId=self.sessionId, layerType="access", assetId=self.assetId, domain=self.domain, accessLayerUid=l["uid"],
            #         filter="dst:" + self.ipv4Address,
            #         filterSettings={
            #         "search-mode": "packet",
            #         "packet-search-settings": {
            #             "match-on-any": True
            #         }
            #     }))
            #
            # for rb in acls:
            #     try:
            #         for el in rb["rulebase"]:
            #             try:
            #                 for s in el["source"]:
            #                     r = Role(sessionId=self.sessionId, assetId=self.assetId, domain=self.domain, uid=s).info()
            #                     if "uid" in r and "name" in r:
            #                         rolesToIpv4.append({
            #                             r["uid"]: {
            #                                 "name": r["name"]
            #                             }
            #                         })
            #             except CustomException as e:
            #                 if e.status == 400:
            #                     pass
            #     except KeyError:
            #         pass

            return rolesToIpv4
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def usedModels() -> list:
        return ["object", "host", "ruleaccess", "roleaccess"]
