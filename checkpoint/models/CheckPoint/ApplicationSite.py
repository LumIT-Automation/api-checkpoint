from checkpoint.models.CheckPoint.backend.ApplicationSite import ApplicationSite as Backend

from checkpoint.helpers.Lang import Lang


class ApplicationSite:
    def __init__(self, sessionId: str, assetId: int, domain: str = "", name: str = "", uid: str = "", applicationId: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = sessionId
        self.assetId: int = int(assetId)
        self.domain: str = domain
        self.name: str = name
        self.uid: str = uid
        self.applicationId: str = applicationId



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self) -> dict:
        try:
            return Backend.info(self.sessionId, self.assetId, self.domain, self.uid)
        except Exception as e:
            raise e



    def modify(self, data: dict, autoPublish: bool = True) -> None:
        try:
            Backend.modify(self.sessionId, self.assetId, self.domain, self.uid, data, autoPublish)

            for k, v in Lang.toDict(data).items():
                setattr(self, k, v)
        except Exception as e:
            raise e
 


    def delete(self, autoPublish: bool = True) -> None:
        try:
            Backend.delete(self.sessionId, self.assetId, self.domain, self.uid, autoPublish)
            del self
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def listQuick(sessionId: str, assetId: int, domain: str, detail: str = "standard", localOnly: bool = False) -> list:
        try:
            out = list()

            if localOnly and domain != "Global":
                o = Backend.list(sessionId, assetId, domain, detail=detail)
                for el in o:
                    if "domain" in el and "domain-type" in el["domain"]:
                        if el["domain"]["domain-type"] != "global domain":
                            out.append(el)
            else:
                out = Backend.list(sessionId, assetId, domain, detail=detail)

            return out
        except Exception as e:
            raise e



    @staticmethod
    def listCustomApplicationSitesQuick(sessionId: str, assetId: int, domain: str, localOnly: bool = False) -> list:
        customAppList = []

        try:
            appList = ApplicationSite.listQuick(sessionId, assetId, domain, detail="full", localOnly=localOnly)
            for app in appList:
                if "primary-category" in app and app["primary-category"] == "Custom_Application_Site":
                    customAppList.append(app)

            return customAppList
        except Exception as e:
            raise e



    @staticmethod
    def add(sessionId: str, assetId: int, domain: str, data: dict, autoPublish: bool = True) -> dict:
        out = dict()

        try:
            o = Backend.add(sessionId, assetId, domain, data, autoPublish)
            out["uid"] = o.get("uid", "")
        except Exception as e:
            raise e

        return out
