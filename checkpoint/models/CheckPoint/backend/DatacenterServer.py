import time
from typing import List

from django.conf import settings

from checkpoint.models.CheckPoint.Session import Session

from checkpoint.helpers.ApiSupplicant import ApiSupplicant
from checkpoint.helpers.Exception import CustomException
from checkpoint.helpers.Log import Log


class DatacenterServer:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def info(sessionId: str, assetId: int, domain: str, uid: str) -> dict:
        try:
            return ApiSupplicant(sessionId, assetId).post(
                urlSegment="show-data-center-server",
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
        timeout = 120 # [second]

        from checkpoint.models.CheckPoint.Task import Task

        try:
            response = ApiSupplicant(sessionId, assetId).post(
                urlSegment="set-data-center-server",
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
                        raise CustomException(status=400, payload={"CheckPoint": taskRunInfo.get("task-details", [])[0].get("fault-message", "unknown error")})

                    if time.time() >= t0 + timeout: # timeout reached.
                        raise CustomException(status=400, payload={"CheckPoint": f"task timeout reached"})

                    time.sleep(5)
                except KeyError:
                    pass
                except IndexError:
                    pass

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
                urlSegment="delete-data-center-server",
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
    def list(sessionId: str, assetId: int, domain: str, details: str = "standard", filter: str = "") -> List[dict]:
        out = list()
        limit = 500

        try:
            # Collect all data (serial requests).
            for n in range(0, settings.MAX_REQUESTS):
                o = ApiSupplicant(sessionId, assetId, silent=True).post(
                    urlSegment="show-data-center-servers",
                    domain=domain,
                    data={
                        "details-level": details,
                        "limit": limit,
                        "offset": limit * n,
                        "filter": filter
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
    def add(sessionId: str, assetId: int, domain: str, data: dict, autoPublish: bool = True) -> None:
        timeout = 120 # [second]
        from checkpoint.models.CheckPoint.Task import Task

        try:
            response = ApiSupplicant(sessionId, assetId).post(
                urlSegment="add-data-center-server",
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
                        raise CustomException(status=400, payload={"CheckPoint": taskRunInfo.get("task-details", [])[0].get("fault-message", "unknown error")})

                    if time.time() >= t0 + timeout: # timeout reached.
                        raise CustomException(status=400, payload={"CheckPoint": f"task timeout reached"})

                    time.sleep(5)
                except KeyError:
                    pass
                except IndexError:
                    pass

            if autoPublish:
                Session(sessionId=sessionId, assetId=assetId, domain=domain).publish()
        except Exception as e:
            if autoPublish:
                Session(sessionId=sessionId, assetId=assetId, domain=domain).discard()

            raise e
