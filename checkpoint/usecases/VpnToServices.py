from checkpoint.models.CheckPoint.Role import Role
from checkpoint.models.CheckPoint.Rule import Rule

from checkpoint.models.CheckPoint.Host import Host
from checkpoint.models.CheckPoint.Group import Group
from checkpoint.models.CheckPoint.Object import Object
from checkpoint.models.CheckPoint.AddressRange import AddressRange
from checkpoint.models.CheckPoint.Network import Network

from checkpoint.helpers.Exception import CustomException
from checkpoint.helpers.Log import Log


class VpnToServices:
    def __init__(self, sessionId: str, assetId: int, domain: str, name: str, user: str, workflowId: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = sessionId
        self.assetId: int = int(assetId)
        self.domain: str = domain
        self.name: str = name
        self.username = user
        self.workflowId = workflowId



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def __call__(self, *args, **kwargs) -> list:
        try:
            no = 0
            services = list()
            rules = list()

            roleInformation = Role.searchByName(self.sessionId, self.assetId, self.domain, self.name, localOnly=False)
            if roleInformation and "uid" in roleInformation:
                role = Role(self.sessionId, self.assetId, self.domain, uid=roleInformation["uid"])
                w = role.whereUsed(indirect=True)

                # Access control rules where role is used.
                for j in ("used-directly", "used-indirectly"):
                    rules.extend(w[j].get("access-control-rules", []))

                # Get destination information for each rule.
                for rule in rules:
                    ruleAcl = Rule(self.sessionId, "access", self.assetId, self.domain, layerUid=rule.get("layer", {}).get("uid", ""), uid=rule.get("rule", {}).get("uid", "")).info()
                    for j in ruleAcl.get("destination", []):
                        try:
                            ipv4s = {}

                            # Get Ipv4 addresses depending on destination type.
                            if j["type"] == "host":
                                h = Host(self.sessionId, self.assetId, self.domain, uid=j["uid"]).info()
                                ipv4s = {
                                    "address": h["ipv4-address"]
                                }
                            if j["type"] == "group":
                                l = []
                                VpnToServices.__groupIpv4Addresses(self.sessionId, self.assetId, self.domain, groupUid=j["uid"], l=l)
                                ipv4s = {
                                    "addresses": l
                                }
                            if j["type"] == "address-range":
                                r = AddressRange(self.sessionId, self.assetId, self.domain, uid=j["uid"]).info()
                                ipv4s = {
                                    "range": r["ipv4-address-first"] + " - " + r["ipv4-address-last"]
                                }
                            if j["type"] == "network":
                                n = Network(self.sessionId, self.assetId, self.domain, uid=j["uid"]).info()
                                ipv4s = {
                                    "network": str(n["subnet4"]) + "/" + str(n["mask-length4"])
                                }

                            services.append({
                                j["uid"]: {
                                    "name": j["name"],
                                    "type": j["type"],
                                    "ipv4": ipv4s,
                                    "services": list()
                                }
                            })

                            # Add port/protocol information to services data structure.
                            if "service" in ruleAcl:
                                for s in ruleAcl["service"]:
                                    if "type" in s:
                                        if s["type"] == "service-group":
                                            for member in s["members"]:
                                                o = Object(self.sessionId, self.assetId, self.domain, uid=member).info()["object"]
                                                services[no][j["uid"]]["services"].append({
                                                    "type": o.get("type", ""),
                                                    "port": o.get("port", ""),
                                                    "protocol": o.get("protocol", ""),
                                                })
                                        else:
                                            services[no][j["uid"]]["services"].append({
                                                "type": s.get("type", ""),
                                                "port": s.get("port", ""),
                                                "protocol": s.get("protocol", ""),
                                            })

                            no += 1
                        except KeyError:
                            pass
            else:
                raise CustomException(status=404, payload={"CheckPoint": "role not found"})

            # Cleanup data structure.
            for j, service in enumerate(services):
                for k, v in service.items():
                    services[j] = dict()

                    services[j]["uid"] = k
                    services[j].update(v)

            return list({v['uid']: v for v in services}.values()) # unique uids.
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def usedModels() -> list:
        return ["object", "host", "address_range", "network", "group", "ruleaccess", "roleaccess"]



    ####################################################################################################################
    # Private static methods
    ####################################################################################################################

    @staticmethod
    def __groupIpv4Addresses(sessionId: str, assetId: int, domain: str, groupUid: str, l: list) -> None: # l: list.
        group = Group(sessionId, assetId, domain, uid=groupUid).info()

        for member in group["members"]:
            if member["type"] == "group":
                for m in member["members"]:
                    o = Object(sessionId, assetId, domain, uid=m).info()

                    if o["object"]["type"] == "host":
                        l.append(o["object"]["ipv4-address"])

                    if o["object"]["type"] == "group":
                        VpnToServices.__groupIpv4Addresses(sessionId, assetId, domain, groupUid=m, l=l) # recurse.

            if member["type"] == "host":
                l.append(member["ipv4-address"])
