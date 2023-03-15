import ipaddress

from checkpoint.models.CheckPoint.Object import Object
from checkpoint.models.CheckPoint.Host import Host
from checkpoint.models.CheckPoint.Layer import Layer
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

            # # Alternative approach for collecting acls.
            # # Find all access control rules (of all layers) with self.ipv4Address as destination.
            # accessSections = list()
            # layers = Layer.listQuick(sessionId=self.sessionId, layerType="access", assetId=self.assetId, domain=self.domain)
            # for l in layers:
            #     accessSections.extend(Layer.listRules(sessionId=self.sessionId, layerType="access", assetId=self.assetId, domain=self.domain, accessLayerUid=l["uid"],
            #         filter="dst:" + self.ipv4Address,
            #         filterSettings={
            #         "search-mode": "packet",
            #         "packet-search-settings": {
            #             "match-on-any": True
            #         }
            #     }))
            #
            # for ac in accessSections:
            #     if "rulebase" in ac:
            #         acls.extend(ac["rulebase"])

            # Information from collected security rules (if belonging to the package self.package).
            for acl in acls:
                #if acl.get("package", {}).get("name", "") == self.package:
                if True:
                    ruleAcl = Object(self.sessionId, self.assetId, self.domain, uid=(acl.get("rule", {}).get("uid", "") or acl.get("uid", ""))).info()["object"]

                    # Collect information for all (active) source access roles.
                    if ruleAcl.get("enabled", False):
                        for j in ruleAcl.get("source", []):
                            if j.get("type", "") == "access-role":
                                try:
                                    # Output only access roles related to a domain.
                                    output = False
                                    for u in j.get("users", []):
                                        o = Object(self.sessionId, self.assetId, self.domain, uid=u).info()["object"]
                                        if "dn" in o:
                                            output = True
                                            break

                                    if output:
                                        rolesToIpv4.append({
                                            j["uid"]: {
                                                "name": j["name"],
                                                "services": list()
                                            }
                                        })

                                        if "service" in ruleAcl:
                                            for s in ruleAcl["service"]:
                                                info = {
                                                    "type": s.get("type", ""),
                                                    "port": s.get("port", ""),
                                                }
                                                if "protocol" in s:
                                                    info["protocol"] = s["protocol"]

                                                rolesToIpv4[no][j["uid"]]["services"].append(info)

                                        no += 1
                                except KeyError:
                                    pass

            return rolesToIpv4
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def usedModels() -> list:
        return ["object", "host", "ruleaccess", "roleaccess"]
