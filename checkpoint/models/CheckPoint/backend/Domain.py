from typing import List

from checkpoint.helpers.ApiSupplicant import ApiSupplicant


class Domain:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def info(sessionId: str, assetId: int, uid: str) -> dict:
        try:
            return ApiSupplicant(sessionId, assetId).post(
                urlSegment="show-domain",
                data={
                    "uid": uid,
                    "details-level": "full"
                }
            )
        except Exception as e:
            raise e



    @staticmethod
    def list(sessionId: str, assetId: int, details: str = "standard") -> List[dict]:
        try:
            o = ApiSupplicant(sessionId, assetId).post(
                urlSegment="show-domains",
                data={
                    "details-level": details,
                    "limit": 256
                }
            )
            return o.get("objects", [])
        except Exception as e:
            raise e
