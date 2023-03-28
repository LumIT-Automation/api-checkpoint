from django.conf import settings

from checkpoint.helpers.ApiSupplicant import ApiSupplicant
from checkpoint.helpers.Log import Log

class Ips:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################


    @staticmethod
    def info(sessionId: str, assetId: int, domain: str) -> dict:
        try:
            return ApiSupplicant(sessionId, assetId).post(
                urlSegment="show-ips-status",
                domain=domain,
                data={}
            )
        except Exception as e:
            raise e



    @staticmethod
    def extendedAttributeInfo(sessionId: str, assetId: int, domain: str, attributeUid: str) -> dict:
        try:
            return ApiSupplicant(sessionId, assetId).post(
                urlSegment="show-ips-protection-extended-attribute",
                domain=domain,
                data = {
                    "uid": attributeUid,
                    "details-level": "full"
                }
            )
        except Exception as e:
            raise e



    @staticmethod
    def runUpdate(sessionId: str, assetId: int, domain: str, data: dict = None) -> dict:
        data = data or {}

        try:
            return  ApiSupplicant(sessionId, assetId).post(
                urlSegment="run-ips-update",
                domain=domain,
                data=data
            )
        except Exception as e:
            raise e



    @staticmethod
    def updateScheduleInfo(sessionId: str, assetId: int, domain: str) -> dict:
        try:
            return ApiSupplicant(sessionId, assetId).post(
                urlSegment="show-ips-update-schedule",
                domain=domain,
                data={}
            )
        except Exception as e:
            raise e



    @staticmethod
    def updateScheduleModify(sessionId: str, assetId: int, domain: str, data: dict) -> dict:
        try:
            return ApiSupplicant(sessionId, assetId).post(
                urlSegment="set-ips-update-schedule",
                domain=domain,
                data=data
            )
        except Exception as e:
            raise e



    @staticmethod
    def listExtendedAttributes(sessionId: str, assetId: int, domain: str, details: str = "standard") -> list:
        out = list()
        limit = 500

        try:
            # Collect all data (serial requests).
            for n in range(0, settings.MAX_REQUESTS):
                o = ApiSupplicant(sessionId, assetId, silent=True).post(
                    urlSegment="show-ips-protection-extended-attributes",
                    domain=domain,
                    data={
                        "details-level": details,
                        "limit": limit,
                        "offset": limit * n
                    }
                )

                if "objects" in o and o["objects"]:
                    out.extend(o["objects"])
                    if o["to"] >= o["total"]:
                        break
                else:
                    break

            return out
        except Exception as e:
            raise e

