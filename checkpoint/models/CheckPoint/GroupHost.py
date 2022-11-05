from typing import List

from checkpoint.models.CheckPoint.Group import Group


class GroupHost:
    def __init__(self, sessionId: str, assetId: int, domain: str, groupUid: str, hostUid: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = sessionId
        self.assetId: int = int(assetId)
        self.domain: str = domain
        self.group: str = groupUid
        self.host: str = hostUid



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def remove(self, autoPublish: bool = True) -> None:
        try:
            Group(sessionId=self.sessionId, assetId=self.assetId, domain=self.domain, uid=self.group).modify(
                data={
                    "members": {
                        "remove": self.host
                    }
                },
                autoPublish=autoPublish
            )
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def listGroupHosts(sessionId: str, assetId: int, domain: str, groupUid: str) -> List[dict]:
        o = list()

        try:
            info = Group(sessionId=sessionId, assetId=assetId, domain=domain, uid=groupUid).info()
            if "members" in info:
                for member in info["members"]:
                    if "type" in member and member["type"] == "host":
                        if "groups" in member:
                            del member["groups"] # cleanup redundant data.

                        o.append(member)

            return o
        except Exception as e:
            raise e



    @staticmethod
    def addHostsToGroup(sessionId: str, assetId: int, domain: str, groupUid: str, hostUids: list, autoPublish: bool = True) -> None:
        try:
            Group(sessionId=sessionId, assetId=assetId, domain=domain, uid=groupUid).modify(
                data={
                    "members": {
                        "add": hostUids
                    }
                },
                autoPublish=autoPublish
            )
        except Exception as e:
            raise e
