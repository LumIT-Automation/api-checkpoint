from checkpoint.helpers.ApiSupplicant import ApiSupplicant


class User:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def info(sessionId: str, assetId: int, domain: str, uid: str) -> dict:
        try:
            return ApiSupplicant(sessionId, assetId).post(
                urlSegment="show-user",
                domain=domain,
                data={
                    "uid": uid,
                    "details-level": "full"
                }
            )
        except Exception as e:
            raise e
