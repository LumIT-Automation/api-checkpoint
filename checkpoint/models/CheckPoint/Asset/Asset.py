from typing import List

from checkpoint.models.CheckPoint.Asset.repository.Asset import Asset as Repository


class Asset:
    def __init__(self, assetId: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id = int(assetId)
        self.address: str = ""
        self.fqdn: str = ""
        self.baseurl: str = ""
        self.tlsverify: int = 1
        self.datacenter: str = ""
        self.environment: str = ""
        self.position: str = ""

        self.username: str = ""
        self.password: str = ""

        self.__load()



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def modify(self, data: dict) -> None:
        try:
            Repository.modify(self.id, data)
        except Exception as e:
            raise e



    def delete(self) -> None:
        try:
            Repository.delete(self.id)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list() -> List[dict]:
        try:
            return Repository.list()
        except Exception as e:
            raise e



    @staticmethod
    def add(data: dict) -> None:
        from checkpoint.models.Permission.Domain import Domain as PermissionDomain
        from checkpoint.models.Permission.Permission import Permission

        try:
            aId = Repository.add(data)

            # When inserting an asset, add the "any" domain (Permission).
            PermissionDomain.add(aId, "any")

            # Also, add a "*" permission for the workflow.local system user.
            Permission.addFacade(
                identityGroupIdentifier="workflow.local",
                role="workflow",
                domainInfo={
                    "assetId": aId,
                    "name": "any"
                }
            )
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __load(self) -> None:
        try:
            info = Repository.get(self.id)

            # Set attributes.
            for k, v in info.items():
                setattr(self, k, v)
        except Exception as e:
            raise e
