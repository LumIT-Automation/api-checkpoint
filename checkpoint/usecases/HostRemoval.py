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
                                    self.__groupHostUnlinking(domain=currentDomain, groupUid=o["uid"], hostUid=hostUid)

                            # Delete lonely groups.
                            for o in whereUsed["objects"]:
                                if o["type"] == "group":
                                    self.__groupsManagement(
                                        domain=currentDomain, groupUid=o["uid"]
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
                                    domain=currentDomain, package=o["package"]["uid"], ruleUid=o["rule"]["uid"], objUid=hostUid
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
                                    domain=currentDomain, groupUid=undead[1]
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
                ruleName = r.info()["name"]
                r.delete(autoPublish=False)
                self.__log(domain=domain, message=f"Deleted orphaned rule '{layer}/{rule}'", object_type="rule", object=rule, object_name=ruleName, status="deleted")
            else:
                # Remove host in rule (within source and/or destination).
                RuleObject(self.sessionId, ruleType=ruleType, assetId=self.assetId, domain=domain, layerUid=layer, ruleUid=rule, objectUid=obj).remove(autoPublish=False)
                self.__log(domain=domain, message=f"Unlinked object '{obj}' from rule '{rule}'", object_type="object", object=obj, object_name="", status="unlinked", parent_object=rule, parent_object_name=Rule(self.sessionId, ruleType=ruleType, assetId=self.assetId, domain=domain, layerUid=layer, uid=rule).info()["name"])

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



    def __natRuleManagement(self, domain: str, package: str, ruleUid: str, objUid: str) -> None:
        # If object is within one of the rule fields, remove the rule.
        try:
            natRule = NatRule(self.sessionId, assetId=self.assetId, domain=domain, packageUid=package, uid=ruleUid)
            info = natRule.info()

            for f in ("original-destination", "translated-destination", "original-source", "translated-source"):
                if info.get(f)["uid"] == objUid:
                    natRuleName = natRule.info()["name"]
                    natRule.delete(autoPublish=False)
                    self.__log(domain=domain, message=f"Deleted orphaned NAT rule '{package}/{ruleUid}'", object_type="nat_rule", object=ruleUid, object_name=natRuleName, status="deleted")

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
                self.globalUndead.append(("nat", package, ruleUid))
            else:
                raise e
        except Exception as e:
            raise e



    def __groupHostUnlinking(self, domain: str, groupUid: str, hostUid: str):
        try:
            g = GroupHost(self.sessionId, assetId=self.assetId, domain=domain, groupUid=groupUid, hostUid=hostUid)

            g.remove(autoPublish=False)
            self.__log(domain=domain, message=f"Unlinked host '{hostUid}' from group '{groupUid}'", object_type="host", object=hostUid, object_name="", status="unlinked", parent_object=groupUid, parent_object_name=Group(self.sessionId, assetId=self.assetId, domain=domain, uid=groupUid).info()["name"])
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
                    domain=domain, package=o["package"]["uid"], ruleUid=o["rule"]["uid"], objUid=groupUid
                )
        except KeyError:
            pass
        except Exception as e:
            raise e



    def __groupsManagement(self, domain: str, groupUid: str, sonGroupUid: str = "") -> None:
        try:
            # If group is to remain empty on host deletion, delete also this group.
            g = Group(self.sessionId, assetId=self.assetId, domain=domain, uid=groupUid)
            groupName = g.info()["name"]

            if sonGroupUid:
                # Unlink son group (while in recursion).
                sonGroupName = Group(self.sessionId, assetId=self.assetId, domain=domain, uid=sonGroupUid).info()["name"]

                g.deleteInnerGroup(sonGroupUid, autoPublish=False)
                self.__log(domain=domain, message=f"Unlinked group '{sonGroupUid}' from group '{groupUid}'", object_type="group", object=sonGroupUid, object_name=sonGroupName, status="unlinked", parent_object=groupUid, parent_object_name=groupName)

            groupDetails = g.info()

            if len(groupDetails["members"]) == 0:
                # Group is deletable (empty). Recursively manage father groups.
                fathers = g.listFatherGroups()
                for f in fathers:
                    self.__groupsManagement(domain=domain, groupUid=f["uid"], sonGroupUid=groupUid)

                # Apply from top-level to bottom.
                # Delete group, but before unlink it from security/NAT rules, if any.
                self.__groupRuleManagement(domain, g)

                g.delete(autoPublish=False)
                self.__log(domain=domain, message=f"Deleted lonely group '{groupUid}'", object_type="group", object=groupUid, object_name=groupName, status="deleted")
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
                self.globalUndead.append(("group", groupUid))
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
            objName = host.info()["name"]
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



    def __log(self, domain: str, message: str, object_type: str, object: str, object_name: str, status: str, parent_object: str = "", parent_object_name: str = "") -> None:
        try:
            logString = f"[WORKFLOW {self.workflowId}] [Domain: {domain}] [Username: {self.username}] [ip address: {self.ipv4Address}] [object name: {object_name}] "
            if parent_object:
                logString += f" [parent object: {parent_object}] "
            if parent_object_name:
                logString += f" [parent object name: {parent_object_name}] "
            Log.log(logString + str(message), "_")
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
                "parent_object": parent_object,
                "parent_object_name": parent_object_name,
                "domain": domain,
                "status": status
            })
        except Exception:
            pass
