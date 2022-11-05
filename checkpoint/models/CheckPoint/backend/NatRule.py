from checkpoint.models.CheckPoint.Session import Session

from checkpoint.helpers.ApiSupplicant import ApiSupplicant


class NatRule:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def info(sessionId: str, assetId: int, domain: str, packageUid: str, uid: str) -> dict:
        try:
            return ApiSupplicant(sessionId, assetId).post(
                urlSegment="show-nat-rule",
                domain=domain,
                data={
                    "uid": uid,
                    "details-level": "full",
                    "package": packageUid
                }
            )
        except Exception as e:
            raise e



    @staticmethod
    def modify(sessionId: str, assetId: int, domain: str, packageUid: str, uid: str, data: dict, autoPublish: bool = True) -> None:
        data.update({
            "uid": uid,
            "package": packageUid
        })

        try:
            ApiSupplicant(sessionId, assetId).post(
                urlSegment="set-nat-rule",
                domain=domain,
                data=data
            )

            if autoPublish:
                Session(sessionId=sessionId, assetId=assetId, domain=domain).publish()
        except Exception as e:
            if autoPublish:
                Session(sessionId=sessionId, assetId=assetId, domain=domain).discard()

            raise e



    @staticmethod
    def delete(sessionId: str, assetId: int, domain: str, packageUid: str, uid: str, autoPublish: bool = True) -> None:
        try:
            ApiSupplicant(sessionId, assetId).post(
                urlSegment="delete-nat-rule",
                domain=domain,
                data={
                    "uid": uid,
                    "package": packageUid
                }
            )

            if autoPublish:
                Session(sessionId=sessionId, assetId=assetId, domain=domain).publish()
        except Exception as e:
            if autoPublish:
                Session(sessionId=sessionId, assetId=assetId, domain=domain).discard()

            raise e
