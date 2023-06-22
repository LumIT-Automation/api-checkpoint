from typing import Callable
import requests
import json

from django.conf import settings

from checkpoint.models.CheckPoint.Asset.Asset import Asset

from checkpoint.helpers.Log import Log
from checkpoint.helpers.Exception import CustomException


class ApiSupplicant:
    def __init__(self, sessionId: str, assetId: int, silent: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = sessionId
        self.assetId = assetId
        self.assetData = Asset(self.assetId)
        self.httpProxy = settings.API_SUPPLICANT_HTTP_PROXY
        self.timeout = settings.API_SUPPLICANT_NETWORK_TIMEOUT
        self.silent = silent

        self.responseStatus = 500
        self.responsePayload = dict()
        self.responseHeaders = dict()



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def post(self, data: dict, domain: str = "", urlSegment: str = "") -> dict:
        from checkpoint.models.CheckPoint.Session import Session

        try:
            url = self.assetData.baseurl+urlSegment

            Log.actionLog("[API Supplicant] Posting to remote: " + str(url))
            Log.actionLog("[API Supplicant] Posting data: " + str(data))

            return self.__request(
                requests.post,
                url=url,
                additionalHeaders={
                    "x-chkp-sid": self.__getToken(domain)
                },
                data=data
            )
        except CustomException as e:
            # Handle token expiration before supposed session-timeout (i.e. something unexpected happens).
            if e.status == 400 and self.responseStatus == 401:
                # Delete the cache, but fresh data will be served only on next user's request. @todo: improve.
                Session.deleteTokens(self.sessionId, self.assetId, domain, onlyFromDomain=False)
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __getToken(self, domain: str = "") -> str:
        from checkpoint.models.CheckPoint.Session import Session

        try:
            if not domain:
                token = Session.getSavedToken(sessionId="", assetId=self.assetId, domain="") # try loading login token from cache.
            else:
                token = Session.getSavedToken(sessionId=self.sessionId, assetId=self.assetId, domain=domain) # try loading domain token from cache.

            if not token:
                # Obtain login token.
                if not domain:
                    Log.actionLog("[API Supplicant] Requesting login token for asset " + str(self.assetId))
                    response = self.__request(
                        requests.post,
                        url=self.assetData.baseurl + "login",
                        data={
                            "user": self.assetData.username,
                            "password": self.assetData.password,
                            "session-timeout": 80
                        }
                    )

                    token = response.get("sid", "")
                    Session.saveToken(sessionId="", assetId=self.assetId, domain="", value=token, timeout=response.get("session-timeout", 60)) # login token, unrelated to session.

                # Domain token.
                else:
                    Log.actionLog("[API Supplicant] Requesting domain token: " + str(domain) + " for asset " + str(self.assetId))
                    response = self.__request(
                        requests.post,
                        url=self.assetData.baseurl + "login-to-domain",
                        additionalHeaders={
                            "x-chkp-sid": self.__getToken() # recursive.
                        },
                        data={
                            "domain": domain
                        }
                    )

                    token = response.get("sid", "")
                    Session.saveToken(self.sessionId, self.assetId, domain, value=token, timeout=response.get("session-timeout", 600))

            return token
        except Exception as e:
            raise e



    def __request(self, request: Callable, url: str, additionalHeaders: dict = None, params: dict = None, data: dict = None) -> dict:
        params = {} if params is None else params
        data = {} if data is None else data
        additionalHeaders = {} if additionalHeaders is None else additionalHeaders

        # In the event of a network problem (e.g. DNS failure, refused connection, etc), Requests will raise a ConnectionError exception.
        # If a request times out, a Timeout/ConnectTimeout exception is raised.
        # If a request exceeds the configured number of maximum redirections, a TooManyRedirects exception is raised.
        # SSLError on SSL/TLS error.

        # On KO status codes, a CustomException is raised, with response status and body.

        headers = {
            "Content-Type": "application/json"
        }

        headers.update(additionalHeaders)

        try:
            response = request(
                url,
                proxies=self.httpProxy,
                verify=self.assetData.tlsverify,
                timeout=settings.API_SUPPLICANT_NETWORK_TIMEOUT,
                headers=headers,
                params=params, # GET parameters.
                data=json.dumps(data)
            )

            self.responseStatus = response.status_code
            self.responseHeaders = response.headers

            try:
                self.responsePayload = response.json()
            except Exception:
                self.responsePayload = {}

            if not self.silent:
                for j in (("status", self.responseStatus), ("headers", self.responseHeaders), ("payload", self.responsePayload)):
                    Log.actionLog("[API Supplicant] Remote response " + j[0] + ": " + str(j[1]))
            else:
                Log.actionLog("[API Supplicant] Remote response status (log silenced): " + str(self.responseStatus))

            # CustomException errors on connection ok but ko status code.
            if self.responseStatus == 200 or self.responseStatus == 201: # ok / ok on POST.
                pass
            elif self.responseStatus == 401:
                raise CustomException(status=400, payload={"CheckPoint": "wrong credentials for the asset"})
            else:
                if "message" in self.responsePayload:
                    checkpointError = self.responsePayload["message"]
                    if "warnings" in self.responsePayload:
                        checkpointError += ". "
                        for el in self.responsePayload["warnings"]:
                            checkpointError += str(el.get("message", "")) + " "
                    if "errors" in self.responsePayload:
                        checkpointError += ". "
                        for el in self.responsePayload["errors"]:
                            checkpointError += str(el.get("message", "")) + " "
                    if "blocking-errors" in self.responsePayload:
                        checkpointError += ". "
                        for el in self.responsePayload["blocking-errors"]:
                            checkpointError += str(el.get("message", "")) + " "
                else:
                    checkpointError = self.responsePayload

                Log.actionLog("[API Supplicant] CheckPoint error: " + str(checkpointError))
                raise CustomException(status=self.responseStatus, payload={"CheckPoint": checkpointError})
        except Exception as e:
            raise e

        return self.responsePayload
