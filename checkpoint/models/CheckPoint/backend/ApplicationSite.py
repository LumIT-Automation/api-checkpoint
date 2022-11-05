from typing import List
import threading
from math import ceil

from checkpoint.models.CheckPoint.Session import Session

from checkpoint.helpers.ApiSupplicant import ApiSupplicant
from checkpoint.helpers.Log import Log


class ApplicationSite:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def info(sessionId: str, assetId: int, domain: str, uid: str) -> dict:
        try:
            return ApiSupplicant(sessionId, assetId).post(
                urlSegment="show-application-site",
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
                urlSegment="set-application-site",
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
                urlSegment="delete-application-site",
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
    def list(sessionId: str, assetId: int, domain: str, detail: str = "standard") -> List[dict]:
        out = list()
        limit = 500

        # Get a chunk of <limit> records.
        def oList(n):
            try:
                l = ApiSupplicant(sessionId, assetId=assetId, silent=True).post(
                    urlSegment="show-application-sites",
                    domain=domain,
                    data={
                        "details-level": detail,
                        "limit": limit,
                        "offset": limit * n
                    }
                )

                if "objects" in l and l["objects"]:
                    out.extend(l["objects"])
            except Exception as ee:
                raise ee

        try:
            # Get the number of pages.
            o = ApiSupplicant(sessionId, assetId=assetId, silent=True).post(
                urlSegment="show-application-sites",
                domain=domain,
                data={
                    "details-level": "uid",
                    "limit": 1,
                }
            )

            # Collect all data (parallel, threaded, requests).
            if "total" in o and o["total"] > 0:
                pages = ceil(o["total"] / 500)

                workers = [threading.Thread(target=oList, args=(n,)) for n in range(0, pages)]
                for w in workers:
                    w.start()
                for w in workers:
                    w.join()
        except Exception as e:
            raise e

        return out



    @staticmethod
    def add(sessionId: str, assetId: int, domain: str, data: dict, autoPublish: bool = True) -> dict:
        try:
            o = ApiSupplicant(sessionId, assetId).post(
                urlSegment="add-application-site",
                domain=domain,
                data=data
            )

            if autoPublish:
                Session(sessionId=sessionId, assetId=assetId, domain=domain).publish()

            return o
        except Exception as e:
            if autoPublish:
                Session(sessionId=sessionId, assetId=assetId, domain=domain).discard()

            raise e
