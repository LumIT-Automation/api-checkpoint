from typing import List

from django.core.cache import cache

from checkpoint.models.CheckPoint.backend.Session import Session as Backend


class Session:
    def __init__(self, sessionId: str, assetId: int, domain: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = sessionId
        self.assetId = int(assetId)
        self.domain = domain



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def publish(self) -> dict:
        # Publish modifications for this session.
        try:
            return Backend.publish(self.sessionId, self.assetId, self.domain)
        except Exception as e:
            raise e



    def discard(self) -> None:
        # Discard all changes in the current CheckPoint session.
        try:
            Backend.discard(self.sessionId, self.assetId, self.domain)
        except Exception as e:
            raise e



    def logout(self) -> None:
        try:
            Backend.logout(self.sessionId, self.assetId, self.domain)
            Session.deleteTokens(self.sessionId, self.assetId, self.domain)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def listQuick(sessionId: str, assetId: int, domain: str, details: str = "standard", filter: str = "") -> List[dict]:
        try:
            return Backend.list(sessionId, assetId, domain, details, filter=filter)
        except Exception as e:
            raise e



    @staticmethod
    def getSavedToken(sessionId: str, assetId: int, domain: str) -> str:
        return cache.get(
            "token-"+str(sessionId)+"-"+str(assetId)+"-"+str(domain) # load from cache.
        )



    @staticmethod
    def saveToken(sessionId: str, assetId: int, domain: str, value: str, timeout: int) -> None:
        cache.set("token-"+str(sessionId)+"-"+str(assetId)+"-"+str(domain), value, timeout=timeout)



    @staticmethod
    def deleteTokens(sessionId: str, assetId: int, domain: str, onlyFromDomain: bool = True) -> None:
        if not onlyFromDomain:
            cache.delete("token-"+str(sessionId)+"-"+str(assetId)+"-") # login.

        cache.delete("token-"+str(sessionId)+"-"+str(assetId)+"-"+str(domain)) # domain.
