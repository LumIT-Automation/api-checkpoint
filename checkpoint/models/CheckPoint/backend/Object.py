import threading
from math import ceil

from checkpoint.helpers.ApiSupplicant import ApiSupplicant


class Object:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def whereUsed(sessionId: str, assetId: int, domain: str, uid: str, indirect: bool = False) -> dict:
        try:
            return ApiSupplicant(sessionId, assetId).post(
                urlSegment="where-used",
                domain=domain,
                data={
                    "uid": uid,
                    "details-level": "standard",
                    "indirect": indirect,
                    "domains-to-process": ["CURRENT_DOMAIN"]
                }
            )
        except Exception as e:
            raise e



    @staticmethod
    def listUnused(sessionId: str, assetId: int, domain: str) -> list:
        out = list()
        limit = 500

        def oList(n):
            try:
                # Get a chunk of <limit> records.
                l = ApiSupplicant(sessionId, assetId, silent=True).post(
                    urlSegment="show-unused-objects",
                    domain=domain,
                    data={
                        "details-level": "standard",
                        "limit": limit,
                        "offset": limit * n,
                        "ignore-warnings": True,
                        "domains-to-process": ["CURRENT_DOMAIN"]
                    }
                )

                if "objects" in l and l["objects"]:
                    out.extend(l["objects"])
            except Exception as ee:
                raise ee

        try:
            # Get the number of pages.
            o = ApiSupplicant(sessionId, assetId, silent=True).post(
                urlSegment="show-unused-objects",
                domain=domain,
                data={
                    "details-level": "uid",
                    "limit": 1,
                    "ignore-warnings": True,
                    "domains-to-process": ["CURRENT_DOMAIN"]
                }
            )

            # Collect all data (parallel, threaded, requests).
            if "total" in o and o["total"] > 0:
                pages = ceil(o["total"] / limit)

                workers = [threading.Thread(target=oList, args=(n,)) for n in range(0, pages)]
                for w in workers:
                    w.start()
                for w in workers:
                    w.join()
        except Exception as e:
            raise e

        return out
