import re

from django.conf import settings
from django.core.cache import cache

from checkpoint.helpers.Log import Log


class Lock:
    def __init__(self, objectClass: any, o: dict, objectName: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId = "any"
        self.domain = "any"
        self.request = ""
        self.objectClass = objectClass
        self.objectName = objectName

        if "assetId" in o:
            self.assetId = str(o["assetId"])

        if "domain" in o:
            self.domain = str(o["domain"])

        if "request" in o:
            self.request = str(o["request"])

        # String or list of strings allowed, treat as list.
        if isinstance(self.objectClass, str):
            self.objectClass = [
                self.objectClass
            ]

        if self.objectName == "":
            self.objectName = "any" # if no object specified -> "any" object.



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def isUnlocked(self) -> bool:
        # @todo: isUnlocked() / lock() should be atomic.

        #     C    R    U    D
        # C   *    x    *    *
        #
        # R   x    v    x    x
        #
        # U   *    x    *    *
        #
        # D   *    x    *    *

        # *: yes, on different objects.
        # R: read for both singular (info) and plural (list); @todo: improve.
        # Workflows: "*" becomes "x": so always a big lock.

        table = {
            "POST": {
                "POST": "*",
                "PUT": "*",
                "GET": "x",
                "PATCH": "*",
                "DELETE": "*",
            },
            "PUT": {
                "POST": "*",
                "PUT": "*",
                "GET": "x",
                "PATCH": "*",
                "DELETE": "*",
            },
            "GET": {
                "POST": "x",
                "PUT": "x",
                "GET": "v",
                "PATCH": "x",
                "DELETE": "x",
            },
            "PATCH": {
                "POST": "*",
                "PUT": "*",
                "GET": "x",
                "PATCH": "*",
                "DELETE": "*",
            },
            "DELETE": {
                "POST": "*",
                "PUT": "*",
                "GET": "x",
                "PATCH": "*",
                "DELETE": "*",
            },
        }

        try:
            # Request HTTP method.
            httpMethod = self.__httpMethod()
            if httpMethod:
                # Check if the API endpoint/s related to objectClass are locked for the asset and domain (if set), on objectName,
                # in regards of the HTTP method "compatibility" (see table).
                for oc in self.objectClass:
                    if oc:
                        if str(httpMethod) in table:
                            for method, compatibility in table[httpMethod].items():
                                entry = oc + ":" + str(method) + ":" + self.assetId + ":" + self.domain # exact same entry check.
                                entryAllDomains = oc + ":" + str(method) + ":" + self.assetId + ":any" # same rule but for all domains.

                                # <httpMethod>: {
                                #    "POST": "x",
                                #    "PUT": "x",
                                #    "GET": "v",
                                #    "PATCH": "*",
                                #    "DELETE": "*",
                                # }

                                c = cache.get(entry)
                                if not c:
                                    c = cache.get(entryAllDomains)

                                if compatibility == "x":
                                    # Always block if entry present (regardless of its value).
                                    if isinstance(c, dict): # if entry present.
                                        if "lock" in c:
                                            if isinstance(c["lock"], list):
                                                if c["lock"]:
                                                    Log.log("Locked on API.")
                                                    Log.log("Available locks: " + str(c))

                                                    return False

                                if compatibility == "*":
                                    # Block if entry present and objectName in the lock list.
                                    if isinstance(c, dict):
                                        if "lock" in c:
                                            if isinstance(c["lock"], list):
                                                if self.objectName in c["lock"]:
                                                    Log.log("Locked on object " + self.objectName)
                                                    Log.log("Available locks: " + str(c))

                                                    return False
        except Exception:
            pass

        return True



    def lock(self) -> None:
        lockedObjects = [self.objectName]

        # Mark the API endpoint/s related to objectClass as locked for the HTTP method,
        # asset and domain (if set), on objectName.
        # For example: pool:POST:1: = { "lock": ... }
        # For example: pool:POST:1:CORPORATE = { "lock": ... }

        # Possible values:
        #   Not set
        #   {'lock': ['any']}
        #   {'lock': ['objectName1', 'objectName2', ...]}
        #   {'lock': ['any', 'objectName3', ...]}

        try:
            httpMethod = self.__httpMethod() # request HTTP method.
            if httpMethod:
                for oc in self.objectClass:
                    if oc:
                        # @todo: a Redis cache transaction lock is needed here.
                        entry = oc + ":" + str(httpMethod) + ":" + self.assetId + ":" + self.domain
                        c = cache.get(entry)

                        # If some locked objectName already set, add the current one.
                        if isinstance(c, dict):
                            if "lock" in c:
                                if self.objectName not in c["lock"]:
                                    c["lock"].append(self.objectName)

                                #lockedObjects = list(dict.fromkeys(c["lock"])) # deduplicate.
                                lockedObjects = c["lock"]

                        cache.set(entry, { "lock": lockedObjects }, timeout=settings.LOCK_MAX_VALIDITY)
                        Log.log("Lock set for " + entry + ", which now values " + str(lockedObjects))
        except Exception:
            pass



    def release(self) -> None:
        # Release the lock for objectName for HTTP method/asset/domain.

        try:
            httpMethod = self.__httpMethod() # request HTTP method.
            if httpMethod:
                for oc in self.objectClass:
                    if oc:
                        entry = oc + ":" + str(httpMethod) + ":" + self.assetId + ":" + self.domain
                        c = cache.get(entry)

                        if "lock" in c:
                            if isinstance(c["lock"], list):
                                c["lock"].remove(self.objectName)

                                if c["lock"]:
                                    # Overwrite if c["lock"] not empty.
                                    cache.set(entry, c, timeout=settings.LOCK_MAX_VALIDITY)
                                else:
                                    # Delete the entry completely.
                                    cache.delete(entry)

                                Log.log("Lock released for " + entry + "; now it values: " + str(cache.get(entry)))
        except Exception:
            pass



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __httpMethod(self):
        httpMethod = ""

        if self.request:
            try:
                matches = re.search(r".*:\ (.*)\ '\/", self.request)
                if matches:
                    httpMethod = str(matches.group(1)).strip()
            except Exception:
                pass

        return httpMethod
