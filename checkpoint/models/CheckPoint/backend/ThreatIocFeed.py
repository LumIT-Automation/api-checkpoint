import time

from django.conf import settings

from checkpoint.models.CheckPoint.Session import Session

from checkpoint.helpers.ApiSupplicant import ApiSupplicant
from checkpoint.helpers.Exception import CustomException


class ThreatIocFeed:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def info(sessionId: str, assetId: int, domain: str, uid: str) -> dict:
        try:
            return ApiSupplicant(sessionId, assetId).post(
                urlSegment="show-threat-ioc-feed",
                domain=domain,
                data={
                    "uid": uid,
                    "details-level": "full"
                }
            )
        except Exception as e:
            raise e



    @staticmethod
    def modify(sessionId: str, assetId: int, domain: str, uid: str, data: dict, autoPublish: bool = True) -> None:
        data["uid"] = uid

        try:
            ApiSupplicant(sessionId, assetId).post(
                urlSegment="set-threat-ioc-feed",
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
    def delete(sessionId: str, assetId: int, domain: str, uid: str, autoPublish: bool = True) -> None:
        try:
            ApiSupplicant(sessionId, assetId).post(
                urlSegment="delete-threat-ioc-feed",
                domain=domain,
                data={
                    "uid": uid
                }
            )

            if autoPublish:
                Session(sessionId=sessionId, assetId=assetId, domain=domain).publish()
        except Exception as e:
            if autoPublish:
                Session(sessionId=sessionId, assetId=assetId, domain=domain).discard()

            raise e



    @staticmethod
    def list(sessionId: str, assetId: int, domain: str, details: str = "standard") -> list:
        out = list()
        limit = 500

        try:
            # Collect all data (serial requests).
            for n in range(0, settings.MAX_REQUESTS):
                o = ApiSupplicant(sessionId, assetId, silent=True).post(
                    urlSegment="show-threat-ioc-feeds",
                    domain=domain,
                    data={
                        "details-level": details,
                        "limit": limit,
                        "offset": limit * n
                    }
                )

                if "profiles" in o and o["profiles"]:
                    out.extend(o["profiles"])
                    if o["to"] >= o["total"]:
                        break
                else:
                    break

            return out
        except Exception as e:
            raise e



    @staticmethod
    def add(sessionId: str, assetId: int, domain: str, data: dict) -> None:
        data = data or {}
        timeout = 120 # [second]

        from checkpoint.models.CheckPoint.Task import Task

        try:
            response = ApiSupplicant(sessionId, assetId).post(
                urlSegment="add-threat-ioc-feed",
                domain=domain,
                data=data
            )

            # Monitor async tasks.
            t0 = time.time()

            while True:
                try:
                    taskRunInfo = Task(sessionId, assetId, domain, uid=response["task-id"]).info()["tasks"][0]

                    if taskRunInfo["status"] == "succeeded":
                        break
                    elif taskRunInfo["status"] == "failed":
                        raise CustomException(status=400, payload={"CheckPoint": taskRunInfo.get("task-details", [])[0].get("statusDescription", "unknown error")})

                    if time.time() >= t0 + timeout: # timeout reached.
                        raise CustomException(status=400, payload={"CheckPoint": f"task timeout reached"})

                    time.sleep(5)
                except KeyError:
                    pass
                except IndexError:
                    pass
        except Exception as e:
            raise e