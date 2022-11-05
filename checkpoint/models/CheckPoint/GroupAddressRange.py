from typing import List

from checkpoint.models.CheckPoint.Group import Group


class GroupAddressRange:
    def __init__(self, sessionId: str, assetId: int, domain: str, groupUid: str, rangeUid: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = sessionId
        self.assetId: int = int(assetId)
        self.domain: str = domain
        self.group: str = groupUid
        self.range: str = rangeUid



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def remove(self) -> None:
        try:
            Group(sessionId=self.sessionId, assetId=self.assetId, domain=self.domain, uid=self.group).modify(
                data={
                    "members": {
                        "remove": self.range
                    }
                }
            )
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def listGroupAddressRanges(sessionId: str, assetId: int, domain: str, groupUid: str) -> List[dict]:
        o = list()

        try:
            info = Group(sessionId=sessionId, assetId=assetId, domain=domain, uid=groupUid).info()
            if "members" in info:
                for member in info["members"]:
                    if "type" in member and member["type"] == "address-range":
                        if "groups" in member:
                            del member["groups"] # cleanup redundant data.

                        o.append(member)

            return o
        except Exception as e:
            raise e



    @staticmethod
    def addAddressRangesToGroup(sessionId: str, assetId: int, domain: str, groupUid: str, rangeUids: list) -> None:
        try:
            Group(sessionId=sessionId, assetId=assetId, domain=domain, uid=groupUid).modify(
                data={
                    "members": {
                        "add": rangeUids
                    }
                }
            )
        except Exception as e:
            raise e
