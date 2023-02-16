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


class HostRemoval:
    def __init__(self, sessionId: str, assetId: int, ipv4Address: str, user: str, workflowId: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = sessionId
        self.assetId: int = int(assetId)
        self.username = user
        self.workflowId = workflowId
        self.ipv4Address: str = ipv4Address

        self.globalUndead: List[tuple] = []



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

                        w = host.whereUsed(indirect=False)
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
                                        domain=currentDomain, group=o["uid"]
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
                            self.__deleteHost(currentDomain, host, hostUid)

                            # Apply all the modifications (a global assignment is also performed when on Global domain).
                            Session(self.sessionId, assetId=self.assetId, domain=currentDomain).publish()
                        except Exception as e:
                            Session(self.sessionId, assetId=self.assetId, domain=currentDomain).discard()
                            raise e

                        existentHost = True

            if self.globalUndead:
                # Global undead carnage.
                # Try unlocking global objects which are in use for various reasons, for example:
                #   DOMAIN:
                #   localGroup
                #       globalGroup1 # -> marked as global undead.
                #       globalGroup2
                #           globalHost

                for domain in domains:
                    currentDomain = domain["name"]

                    try:
                        for undead in self.globalUndead:
                            if undead[0] == "group":
                                # Delete lonely groups.
                                self.__groupsManagement(
                                    domain=currentDomain, group=undead[1]
                                )

                        # Apply all the modifications (a global assignment is also performed when on Global domain).
                        Session(self.sessionId, assetId=self.assetId, domain=currentDomain).publish()
                    except Exception as e:
                        Session(self.sessionId, assetId=self.assetId, domain=currentDomain).discard()
                        raise e
        except KeyError:
            pass
        except Exception as e:
            raise e

        if not existentHost:
            raise CustomException(status=404, payload={"CheckPoint": "non existent IPv4 address (across all domains)"})



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def usedModels() -> list:
        return ["object", "host", "group", "ruleaccess", "rulethreat", "rulehttps", "natrule"]



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __securityRuleManagement(self, ruleType: str, domain: str, layer: str, rule: str, obj: str) -> None:
        try:
            o = RuleObject.listObjectsInRule(self.sessionId, ruleType, self.assetId, domain, layer, rule)
            if (obj in o["source"] and len(o["source"]) < 2) \
                    or (obj in o["destination"] and len(o["destination"]) < 2):

                # Delete rule if no source or destination is to remain.
                r = Rule(self.sessionId, ruleType=ruleType, assetId=self.assetId, domain=domain, layerUid=layer, uid=rule)
                objName = r.name
                r.delete(autoPublish=False)
                self.__log(domain=domain, message=f"Deleted orphaned rule '{layer}/{rule}'", object_type="rule", object=rule, object_name=objName, status="deleted")
            else:
                # Remove host in rule (within source and/or destination).
                r = RuleObject(self.sessionId, ruleType=ruleType, assetId=self.assetId, domain=domain, layerUid=layer, ruleUid=rule, objectUid=obj)
                objName = r.name
                r.remove(autoPublish=False)
                self.__log(domain=domain, message=f"Unlinked object '{obj}' from rule '{rule}'", object_type="object", object=obj, object_name=objName, status="unlinked")

            # @todo: installed-on [?].
        except KeyError:
            pass
        except CustomException as e:
            if e.status == 400 and "read-only" in str(e.payload):
                if domain != "Global":
                    pass # ignore global objects on local domains.
                else:
                    raise e
            elif (e.status == 400 or e.status == 409) and "use" in str(e.payload): # (only when called on Global domain).
                self.globalUndead.append(("security", layer, rule))
            else:
                raise e
        except Exception as e:
            raise e



    def __natRuleManagement(self, domain: str, package: str, rule: str, obj: str) -> None:
        # If object is within one of the rule fields, remove the rule.
        try:
            natRule = NatRule(self.sessionId, assetId=self.assetId, domain=domain, packageUid=package, uid=rule)
            objName = natRule.name

            info = natRule.info()
            for f in ("original-destination", "translated-destination", "original-source", "translated-source"):
                if info.get(f)["uid"] == obj:
                    n = natRule.delete(autoPublish=False)
                    self.__log(domain=domain, message=f"Deleted orphaned NAT rule '{package}/{rule}'", object_type="nat_rule", object=rule, object_name=objName, status="deleted")

                    break

            # @todo: installed-on [?].
        except KeyError:
            pass
        except CustomException as e:
            if e.status == 400 and "read-only" in str(e.payload):
                if domain != "Global":
                    pass # ignore global objects on local domains.
                else:
                    raise e
            elif (e.status == 400 or e.status == 409) and "use" in str(e.payload): # (only when called on Global domain).
                self.globalUndead.append(("nat", package, rule))
            else:
                raise e
        except Exception as e:
            raise e



    def __groupHostUnlinking(self, domain: str, group: str, host: str):
        try:
            g = GroupHost(self.sessionId, assetId=self.assetId, domain=domain, groupUid=group, hostUid=host)
            objName = g.name
            g.remove(autoPublish=False)
            self.__log(domain=domain, message=f"Unlinked host '{host}' from group '{group}'", object_type="host", object=host, object_name=objName, status="unlinked")
        except CustomException as e:
            if e.status == 400 and "read-only" in str(e.payload):
                if domain != "Global":
                    pass # ignore global objects on local domains.
                else:
                    raise e
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



    def __groupsManagement(self, domain: str, group: str, sonGroup: str = "") -> None:
        try:
            # If group is to remain empty on host deletion, delete also this group.
            g = Group(self.sessionId, assetId=self.assetId, domain=domain, uid=group)

            if sonGroup:
                objName = sonGroup.name
                # Unlink son group (while in recursion).
                g.deleteInnerGroup(sonGroup, autoPublish=False)
                self.__log(domain=domain, message=f"Unlinked group '{sonGroup}' from group '{group}'", object_type="group", object=sonGroup, object_name=objName, status="unlinked")

            groupDetails = g.info()

            if len(groupDetails["members"]) == 0:
                # Group is deletable (empty). Recursively manage father groups.
                fathers = g.listFatherGroups()
                for f in fathers:
                    self.__groupsManagement(domain=domain, group=f["uid"], sonGroup=group)

                # Apply from top-level to bottom.
                # Delete group, but before unlink it from security/NAT rules, if any.
                self.__groupRuleManagement(domain, g)

                g.delete(autoPublish=False)
                self.__log(domain=domain, message=f"Deleted lonely group '{group}'", object_type="group", object=group, object_name=g.name, status="deleted")
        except KeyError:
            pass
        except CustomException as e:
            if e.status == 404:
                pass # ignore error if already removed.
            elif e.status == 400 and "read-only" in str(e.payload):
                if domain != "Global":
                    pass # ignore global objects on local domains.
                else:
                    raise e
            elif (e.status == 400 or e.status == 409) and "use" in str(e.payload): # (only when called on Global domain).
                self.globalUndead.append(("group", group))
            else:
                raise e
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



    def __deleteHost(self, domain: str, host: Host, hostUid: str):
        try:
            objName = "host.name"
            host.delete(autoPublish=False)
            self.__log(domain=domain, message=f"Deleted host '{hostUid}'", object_type="host", object=hostUid, object_name=objName, status="deleted")

        except CustomException as e:
            if e.status == 400 and "read-only" in str(e.payload):
                if domain != "Global":
                    pass # ignore global objects on local domains.
                else:
                    raise e
            else:
                raise e
        except Exception as e:
            raise e



    def __log(self, domain: str, message: str, object_type: str, object: str, object_name: str, status: str) -> None:
        try:
            Log.log(f"[WORKFLOW {self.workflowId}] [Domain: {domain}] [Username: {self.username}] [ip address: {self.ipv4Address}] [object name: {object_name}] " + str(message), "_")
        except Exception:
            pass

        try:
            History.add({
                "username": self.username,
                "action": message,
                "asset_id": self.assetId,
                "workflow_id": self.workflowId,
                "config_object_type": object_type,
                "config_object": object,
                "config_object_name": object_name,
                "config_object_description": self.ipv4Address,
                "domain": domain,
                "status": status
            })
        except Exception:
            pass
