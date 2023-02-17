from checkpoint.models.CheckPoint.Domain import Domain as CheckPointDomain

from checkpoint.models.Permission.repository.Domain import Domain as Repository


class Domain:
    def __init__(self, id: int = 0, assetId: int = 0, name: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id: int = int(id)
        self.id_asset: int = int(assetId) # simple property, not composition.
        self.domain: str = name
        self.description: str = ""

        self.__load()



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def delete(self) -> None:
        try:
            Repository.delete(self.id)
            del self
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def add(assetId: int, domain: str) -> int:
        if domain == "any":
            try:
                return Repository.add(assetId, domain)
            except Exception as e:
                raise e
        else:
            # Check if assetId/domain is a valid CheckPoint domain (at the time of the insertion).
            checkpointDomains = CheckPointDomain.listQuick(sessionId="", assetId=assetId)
            for v in checkpointDomains:
                if v["name"] == domain:
                    try:
                        return Repository.add(assetId, domain)
                    except Exception as e:
                        raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __load(self) -> None:
        try:
            info = Repository.get(self.id, self.id_asset, self.domain)

            # Set attributes.
            for k, v in info.items():
                setattr(self, k, v)
        except Exception as e:
            raise e
