from typing import List

from checkpoint.models.CheckPoint.Group import Group


class GroupNetwork:
    def __init__(self, sessionId: str, assetId: int, domain: str, groupUid: str, networkUid: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = sessionId
        self.assetId: int = int(assetId)
        self.domain: str = domain
        self.group: str = groupUid
        self.network: str = networkUid



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def remove(self) -> None:
        try:
            Group(sessionId=self.sessionId, assetId=self.assetId, domain=self.domain, uid=self.group).modify(
                data={
                    "members": {
                        "remove": self.network
                    }
                }
            )
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def listGroupNetworks(sessionId: str, assetId: int, domain: str, groupUid: str) -> List[dict]:
        o = list()

        try:
            info = Group(sessionId=sessionId, assetId=assetId, domain=domain, uid=groupUid).info()
            if "members" in info:
                for member in info["members"]:
                    if "type" in member and member["type"] == "network":
                        if "groups" in member:
                            del member["groups"] # cleanup redundant data.

                        o.append(member)

            return o
        except Exception as e:
            raise e



    @staticmethod
    def addNetworksToGroup(sessionId: str, assetId: int, domain: str, groupUid: str, networkUids: list) -> None:
        try:
            Group(sessionId=sessionId, assetId=assetId, domain=domain, uid=groupUid).modify(
                data={
                    "members": {
                        "add": networkUids
                    }
                }
            )
        except Exception as e:
            raise e
