import time
from typing import List

from django.conf import settings

from checkpoint.helpers.ApiSupplicant import ApiSupplicant


class Session:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def publish(sessionId: str, assetId: int, domain: str) -> dict:
        try:
            response = ApiSupplicant(sessionId, assetId).post(
                urlSegment="publish",
                domain=domain,
                data={}
            )

            time.sleep(1)

            if domain == "Global":
                # Do assign-global-assignment to all domains.
                Session.__assign(sessionId, assetId)

            return response
        except Exception as e:
            raise e



    @staticmethod
    def discard(sessionId: str, assetId: int, domain: str):
        try:
            return ApiSupplicant(sessionId, assetId).post(
                urlSegment="discard",
                domain=domain,
                data={}
            )
        except Exception as e:
            raise e



    @staticmethod
    def logout(sessionId: str, assetId: int, domain: str, onlyFromDomain: bool = True) -> None:
        try:
            ApiSupplicant(sessionId, assetId).post(
                urlSegment="logout",
                domain=domain,
                data={}
            )

            if not onlyFromDomain:
                ApiSupplicant(sessionId, assetId).post(
                    urlSegment="logout",
                    domain="",
                    data={}
                )
        except Exception as e:
            raise e



    @staticmethod
    def list(sessionId: str, assetId: int, domain: str, details: str = "standard", filter: str = "") -> List[dict]:
        out = list()
        limit = 500

        try:
            # Collect all data (serial requests).
            for n in range(0, settings.MAX_REQUESTS):
                o = ApiSupplicant(sessionId, assetId, silent=True).post(
                    urlSegment="show-sessions",
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



    ####################################################################################################################
    # Private static methods
    ####################################################################################################################

    @staticmethod
    def __assign(sessionId: str, assetId: int) -> None:
        from checkpoint.models.CheckPoint.Domain import Domain
        from checkpoint.models.CheckPoint.Task import Task

        domains = list()
        timeout = 120 # [second]

        try:
            # Perform a global assignment on all domains.
            ds = Domain.listQuick(sessionId, assetId)
            for d in ds:
                domains.append(d["name"])

            response = ApiSupplicant(sessionId, assetId).post(
                urlSegment="assign-global-assignment",
                data={
                    "global-domains": "Global",
                    "dependent-domains": domains
                }
            )

            # Wait for async tasks' success or give up silently.
            for task in response["tasks"]:
                t0 = time.time()

                while True:
                    try:
                        taskRunInfo = Task(sessionId, assetId, task["dependent-domain"]["name"], uid=task["task-id"]).info()
                        if taskRunInfo["tasks"][0]["status"] == "succeeded":
                            break
                    except KeyError:
                        pass

                    if time.time() >= t0 + timeout: # timeout reached.
                        break

                    time.sleep(5)
        except Exception as e:
            raise e
