import time

from django.conf import settings

from checkpoint.models.CheckPoint.Session import Session

from checkpoint.helpers.ApiSupplicant import ApiSupplicant
from checkpoint.helpers.Exception import CustomException


class ThreatProtection:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def info(sessionId: str, assetId: int, domain: str, uid: str) -> dict:
        try:
            return ApiSupplicant(sessionId, assetId).post(
                urlSegment="show-threat-protection",
                domain=domain,
                data={
                    "uid": uid,
                    "show-capture-packets-and-track": True,
                    "show-ips-additional-properties": True,
                    "show-profiles": True,
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
                urlSegment="set-threat-protection",
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
    def deleteAll(sessionId: str, assetId: int, domain: str, data: dict = None) -> None:
        data = data or {}
        timeout = 120 # [second]

        from checkpoint.models.CheckPoint.Task import Task

        try:
            response = ApiSupplicant(sessionId, assetId).post(
                urlSegment="delete-threat-protections",
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
                        raise CustomException(status=400, payload={
                            "CheckPoint": taskRunInfo.get("task-details", [])[0].get("statusDescription",
                                                                                     "unknown error")})

                    if time.time() >= t0 + timeout:  # timeout reached.
                        raise CustomException(status=400, payload={"CheckPoint": f"task timeout reached"})

                    time.sleep(5)
                except KeyError:
                    pass
                except IndexError:
                    pass
        except Exception as e:
            raise e



    @staticmethod
    def list(sessionId: str, assetId: int, domain: str, details: str = "standard") -> list:
        out = list()
        limit = 500

        try:
            # Collect all data (serial requests).
            for n in range(0, settings.MAX_REQUESTS):
                o = ApiSupplicant(sessionId, assetId, silent=True).post(
                    urlSegment="show-threat-protections",
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



    @staticmethod
    def add(sessionId: str, assetId: int, domain: str, data: dict) -> dict:
        data = data or {}
        timeout = 120 # [second]

        from checkpoint.models.CheckPoint.Task import Task

        try:
            response = ApiSupplicant(sessionId, assetId).post(
                urlSegment="add-threat-protections",
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