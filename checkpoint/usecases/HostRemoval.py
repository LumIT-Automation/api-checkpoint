from checkpoint.models.CheckPoint.Domain import Domain
from checkpoint.models.CheckPoint.Host import Host
from checkpoint.models.CheckPoint.Group import Group
from checkpoint.models.CheckPoint.GroupHost import GroupHost
from checkpoint.models.CheckPoint.RuleObject import RuleObject
from checkpoint.models.CheckPoint.Rule import Rule
from checkpoint.models.CheckPoint.NatRule import NatRule
from checkpoint.models.CheckPoint.Session import Session

from checkpoint.helpers.Exception import CustomException
from checkpoint.helpers.Log import Log


class HostRemoval:
    def __init__(self, sessionId: str, assetId: int, ipv4Address: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = sessionId
        self.assetId: int = int(assetId)
        self.ipv4Address: str = ipv4Address



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def __call__(self, *args, **kwargs) -> None:
        whereUsed = dict()
        existentHost = False

        try:
            domains = Domain.listQuick(self.sessionId, self.assetId)

            # Find where the IPv4 address (host) is used, amongst all domains.
            for domain in domains:
                currentDomain = domain["name"]

                # Find where the host is used within the domain.
                # More than one host can coexist with the same IPv4 address, but with different names.
                hostsWithIpv4 = Host.searchByIpv4Addresses(self.sessionId, self.assetId, currentDomain, self.ipv4Address, localOnly=False)
                for h in hostsWithIpv4:
                    if h:
                        hostUid = h["uid"]
                        host = Host(self.sessionId, assetId=self.assetId, domain=currentDomain, uid=hostUid)

                        w = host.whereUsed()
                        for el in ("objects", "access-control-rules", "nat-rules", "threat-prevention-rules", "https-rules"):
                            whereUsed[el] = w["used-directly"].get(el, [])

                        try:
                            # Groups.
                            # Unlink host from all groups: a host could be linked to more than one group in the hierarchy.
                            for o in whereUsed["objects"]:
                                if o["type"] == "group":
                                    self.__groupHostUnlinking(domain=currentDomain, group=o["uid"], host=hostUid)

                            # Delete lonely groups.
                            for o in whereUsed["objects"]:
                                if o["type"] == "group":
                                    self.__groupsManagement(
                                        domain=currentDomain, group=o["uid"], host=hostUid
                                    )

                            # Security rules.
                            # Delete rule if no source or destination is to remain.
                            for r in ("access-control-rules", "https-rules", "threat-prevention-rules"):
                                for o in whereUsed[r]:
                                    self.__securityRuleManagement(
                                        domain=currentDomain, ruleType=r.split("-")[0], layer=o["layer"]["uid"], rule=o["rule"]["uid"], obj=h["uid"]
                                    )

                            # NAT rules.
                            # If host is in one of the rule fields, remove the rule.
                            for o in whereUsed["nat-rules"]:
                                self.__natRuleManagement(
                                    domain=currentDomain, package=o["package"]["uid"], rule=o["rule"]["uid"], obj=hostUid
                                )

                            # Finally delete host.
                            HostRemoval.__deleteHost(currentDomain, host, hostUid)

                            # Apply all the modifications (a global assignment is also performed when on Global domain).
                            HostRemoval.__log(currentDomain, f"Publishing modifications (if any)")
                            Session(self.sessionId, assetId=self.assetId, domain=currentDomain).publish()
                        except Exception as e:
                            Session(self.sessionId, assetId=self.assetId, domain=currentDomain).discard()
                            raise e

                        existentHost = True
        except KeyError:
            pass
        except Exception as e:
            raise e

        if not existentHost:
            raise CustomException(status=404, payload={"CheckPoint": "Non existent IPv4 address (across all domains)."})



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def usedModels() -> list:
        return ["object", "host", "group", "rule_access", "rule_threat", "rule_https", "nat_rule"]



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __securityRuleManagement(self, ruleType: str, domain: str, layer: str, rule: str, obj: str) -> None:
        try:
            o = RuleObject.listObjectsInRule(self.sessionId, ruleType, self.assetId, domain, layer, rule)
            if (obj in o["source"] and len(o["source"]) < 2) \
                    or (obj in o["destination"] and len(o["destination"]) < 2):

                # Delete rule if no source or destination is to remain.
                Rule(self.sessionId, ruleType=ruleType, assetId=self.assetId, domain=domain, layerUid=layer, uid=rule).delete(autoPublish=False)
                HostRemoval.__log(domain, f"Deleted orphaned rule '{layer}/{rule}'")
            else:
                # Remove host in rule (within source and/or destination).
                RuleObject(self.sessionId, ruleType=ruleType, assetId=self.assetId, domain=domain, layerUid=layer, ruleUid=rule, objectUid=obj).remove(autoPublish=False)
                HostRemoval.__log(domain, f"Unlinked object '{obj}' from rule '{rule}'")

            # @todo: installed-on [?].
        except KeyError:
            pass
        except CustomException as e:
            if e.status == 400 and "read-only" in str(e.payload):
                pass
            else:
                raise e
        except Exception as e:
            raise e



    def __natRuleManagement(self, domain: str, package: str, rule: str, obj: str) -> None:
        # If object is within one of the rule fields, remove the rule.
        try:
            natRule = NatRule(self.sessionId, assetId=self.assetId, domain=domain, packageUid=package, uid=rule)

            info = natRule.info()
            for f in ("original-destination", "translated-destination", "original-source", "translated-source"):
                if info.get(f)["uid"] == obj:
                    natRule.delete(autoPublish=False)
                    HostRemoval.__log(domain, f"Deleted orphaned NAT rule '{package}/{rule}'")

                    break

            # @todo: installed-on [?].
        except KeyError:
            pass
        except CustomException as e:
            if e.status == 400 and "read-only" in str(e.payload):
                pass
            else:
                raise e
        except Exception as e:
            raise e



    def __groupHostUnlinking(self, domain: str, group: str, host: str):
        try:
            GroupHost(self.sessionId, assetId=self.assetId, domain=domain, groupUid=group, hostUid=host).remove(autoPublish=False)
            HostRemoval.__log(domain, f"Unlinked host '{host}' from group '{group}'")
        except CustomException as e:
            if e.status == 400 and "read-only" in str(e.payload):
                pass
            else:
                raise e
        except Exception as e:
            raise e



    def __groupRuleManagement(self, domain: str, group: Group):
        whereUsed = dict()

        try:
            groupUid = group.info()["uid"]

            w = group.whereUsed()
            for el in ("objects", "access-control-rules", "nat-rules", "threat-prevention-rules", "https-rules"):
                whereUsed[el] = w["used-directly"].get(el, [])

            for r in ("access-control-rules", "https-rules", "threat-prevention-rules"):
                for o in whereUsed[r]:
                    self.__securityRuleManagement(
                        domain=domain, ruleType=r.split("-")[0], layer=o["layer"]["uid"], rule=o["rule"]["uid"], obj=groupUid
                    )

            for o in whereUsed["nat-rules"]:
                self.__natRuleManagement(
                    domain=domain, package=o["package"]["uid"], rule=o["rule"]["uid"], obj=groupUid
                )
        except KeyError:
            pass
        except Exception as e:
            raise e



    def __groupsManagement(self, domain: str, group: str, host: str, sonGroup: str = "") -> None:
        try:
            # If group is to remain empty on host deletion, delete also this group.
            g = Group(self.sessionId, assetId=self.assetId, domain=domain, uid=group)

            if sonGroup:
                # Unlink son group (while in recursion).
                g.deleteInnerGroup(sonGroup, autoPublish=False)
                HostRemoval.__log(domain, f"Unlinked group '{sonGroup}' from group '{group}'")

            groupDetails = g.info()

            if len(groupDetails["members"]) == 0:
                # Group is deletable (empty). Recursively manage father groups.
                fathers = g.listFatherGroups()
                for f in fathers:
                    self.__groupsManagement(domain=domain, group=f["uid"], host=host, sonGroup=group)

                # Apply from top-level to bottom.
                # Delete group, but before unlink it from security/NAT rules, if any.
                self.__groupRuleManagement(domain, g)

                g.delete(autoPublish=False)
                HostRemoval.__log(domain, f"Deleted lonely group '{group}'")
        except KeyError:
            pass
        except CustomException as c:
            if c.status == 404:
                pass # ignore error if already removed.
            elif c.status == 400 and "read-only" in str(c.payload):
                pass
            else:
                raise c
        except Exception as e:
            raise e

        # Graphs, not trees.
        # A complex test example:
        # Group 0
        #     HOST
        #     Group 3
        #     Group 2
        #     Group 1
        #         Group 3
        #         Group 2
        #             Group 3
        #                 HOST



    ####################################################################################################################
    # Private static methods
    ####################################################################################################################

    @staticmethod
    def __deleteHost(domain: str, host: Host, hostUid: str):
        try:
            host.delete(autoPublish=False)
            HostRemoval.__log(domain, f"Deleted host '{hostUid}'")
        except CustomException as e:
            if e.status == 400 and "read-only" in str(e.payload):
                pass
            else:
                raise e
        except Exception as e:
            raise e



    @staticmethod
    def __log(domain: str, message: str):
        Log.log(f"[WORKFLOW] [Domain: {domain}] "+str(message), "_")
