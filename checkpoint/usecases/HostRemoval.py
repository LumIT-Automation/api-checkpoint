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

                        hostDetails = host.info()
                        hostScope = hostDetails["domain"]["domain-type"]

                        w = host.whereUsed()
                        for el in ("objects", "access-control-rules", "nat-rules", "threat-prevention-rules", "https-rules"):
                            whereUsed[el] = w["used-directly"].get(el, [])

                        try:
                            # Groups.
                            # Unlink host from all groups: a host could be linked to more than one group in the hierarchy.
                            for o in whereUsed["objects"]:
                                if o["type"] == "group":
                                    self.__groupHostUnlinking(domain=currentDomain, group=o["uid"], groupScope=o["domain"]["domain-type"], host=hostUid, hostScope=hostScope)

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
                                        domain=currentDomain, ruleType=r.split("-")[0], layer=o["layer"]["uid"], rule=o["rule"]["uid"], ruleScope=o["rule"]["domain"]["domain-type"], obj=h["uid"], objScope=hostScope
                                    )

                            # NAT rules.
                            # If host is in one of the rule fields, remove the rule.
                            for o in whereUsed["nat-rules"]:
                                self.__natRuleManagement(
                                    domain=currentDomain, package=o["package"]["uid"], rule=o["rule"]["uid"], ruleScope=o["rule"]["domain"]["domain-type"], obj=hostUid
                                )

                            # Finally delete host.
                            HostRemoval.__deleteHost(currentDomain, host, hostUid, hostScope)

                            # Apply all the modifications (a global assignment is also performed when on Global domain).
                            HostRemoval.__log(currentDomain, f"Publishing modifications")
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

    def __securityRuleManagement(self, ruleType: str, domain: str, layer: str, rule: str, ruleScope: str, obj: str, objScope: str) -> None:
        try:
            o = RuleObject.listObjectsInRule(self.sessionId, ruleType, self.assetId, domain, layer, rule)
            if (obj in o["source"] and len(o["source"]) < 2) \
                    or (obj in o["destination"] and len(o["destination"]) < 2):

                # Delete rule if no source or destination is to remain.
                if HostRemoval.__objectRemovable(domain, ruleScope):
                    HostRemoval.__log(domain, f"Deleting orphaned rule '{layer}/{rule}'")
                    Rule(self.sessionId, ruleType=ruleType, assetId=self.assetId, domain=domain, layerUid=layer, uid=rule).delete(
                        autoPublish=HostRemoval.__autopublish(domain)
                    )
            else:
                # Remove host in rule (within source and/or destination).
                if HostRemoval.__objectUnlinkable(domain, innerObjectScope=objScope, outerObjectScope=ruleScope):
                    HostRemoval.__log(domain, f"Unlinking object '{obj}' from rule '{rule}'")
                    RuleObject(self.sessionId, ruleType=ruleType, assetId=self.assetId, domain=domain, layerUid=layer, ruleUid=rule, objectUid=obj).remove(
                        autoPublish=HostRemoval.__autopublish(domain)
                    )

            # @todo: installed-on [?].
        except KeyError:
            pass
        except Exception as e:
            raise e



    def __natRuleManagement(self, domain: str, package: str, rule: str, ruleScope: str, obj: str) -> None:
        # If object is within one of the rule fields, remove the rule.
        if HostRemoval.__objectRemovable(domain, ruleScope):
            try:
                natRule = NatRule(self.sessionId, assetId=self.assetId, domain=domain, packageUid=package, uid=rule)

                info = natRule.info()
                for f in ("original-destination", "translated-destination", "original-source", "translated-source"):
                    if info.get(f)["uid"] == obj:
                        HostRemoval.__log(domain, f"Deleting orphaned NAT rule '{package}/{rule}'")
                        natRule.delete(autoPublish=HostRemoval.__autopublish(domain))

                        break

                # @todo: installed-on [?].
            except KeyError:
                pass
            except Exception as e:
                raise e



    def __groupHostUnlinking(self, domain: str, group: str, groupScope: str, host: str, hostScope: str):
        if HostRemoval.__objectUnlinkable(domain, innerObjectScope=hostScope, outerObjectScope=groupScope):
            try:
                HostRemoval.__log(domain, f"Unlinking host '{host}' from group '{group}'")
                GroupHost(self.sessionId, assetId=self.assetId, domain=domain, groupUid=group, hostUid=host).remove(
                    autoPublish=HostRemoval.__autopublish(domain)
                )
            except Exception as e:
                raise e



    def __groupRuleManagement(self, domain: str, group: Group):
        whereUsed = dict()

        try:
            groupDetails = group.info()

            groupUid = groupDetails["uid"]
            groupScope = groupDetails["domain"]["domain-type"]

            w = group.whereUsed()
            for el in ("objects", "access-control-rules", "nat-rules", "threat-prevention-rules", "https-rules"):
                whereUsed[el] = w["used-directly"].get(el, [])

            for r in ("access-control-rules", "https-rules", "threat-prevention-rules"):
                for o in whereUsed[r]:
                    self.__securityRuleManagement(
                        domain=domain, ruleType=r.split("-")[0], layer=o["layer"]["uid"], rule=o["rule"]["uid"], ruleScope=o["rule"]["domain"]["domain-type"], obj=groupUid, objScope=groupScope
                    )

            for o in whereUsed["nat-rules"]:
                self.__natRuleManagement(
                    domain=domain, package=o["package"]["uid"], rule=o["rule"]["uid"], ruleScope=o["rule"]["domain"]["domain-type"], obj=groupUid
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
                # Always unlink son group (while in recursion).
                if HostRemoval.__objectUnlinkable(
                        domain,
                        innerObjectScope=g.info()["domain"]["domain-type"],
                        outerObjectScope=Group(self.sessionId, assetId=self.assetId, domain=domain, uid=sonGroup).info()["domain"]["domain-type"]):
                    HostRemoval.__log(domain, f"Unlinking group '{sonGroup}' from group '{group}'")
                    g.deleteInnerGroup(sonGroup, autoPublish=HostRemoval.__autopublish(domain))

            groupDetails = g.info()

            if len(groupDetails["members"]) == 0:
                # Group is deletable (empty).
                # Recursively manage father groups.
                fathers = g.listFatherGroups()
                for f in fathers:
                    self.__groupsManagement(domain=domain, group=f["uid"], host=host, sonGroup=group)

                # Apply from top-level to bottom.
                # Delete group, but before unlink it from security/NAT rules, if any.
                self.__groupRuleManagement(domain, g)

                if HostRemoval.__objectRemovable(domain, groupDetails["domain"]["domain-type"]):
                    HostRemoval.__log(domain, f"Deleting lonely group '{group}'")
                    g.delete(autoPublish=HostRemoval.__autopublish(domain))
        except KeyError:
            pass
        except CustomException as c:
            if c.status == 404:
                pass # ignore error if already removed.
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
    def __deleteHost(domain: str, host: Host, hostUid: str, hostScope: str):
        try:
            if HostRemoval.__objectRemovable(domain, hostScope):
                HostRemoval.__log(domain, f"Deleting host '{hostUid}'")
                host.delete(autoPublish=HostRemoval.__autopublish(domain))
        except Exception as e:
            raise e



    @staticmethod
    def __autopublish(domain: str) -> bool:
        return bool(domain == "Global")



    @staticmethod
    def __objectRemovable(domain: str, objectScope: str):
        removable = False

        # While working on non-Global domains, only non-global objects are removable.
        if domain == "Global":
            removable = True
        else:
            if "global" not in objectScope:
                removable = True

        return removable



    @staticmethod
    def __objectUnlinkable(domain: str, innerObjectScope: str, outerObjectScope: str):
        unlinkable = False

        # While working on non-Global domains, only non-global objects are removable.
        if domain == "Global":
            unlinkable = True
        else:
            if not (outerObjectScope == "global domain" and innerObjectScope == "global domain"):
                unlinkable = True

        return unlinkable



    @staticmethod
    def __log(domain: str, message: str):
        Log.log(f"[WORKFLOW] [Domain: {domain}] "+str(message), "_")
