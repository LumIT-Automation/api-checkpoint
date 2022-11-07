from checkpoint.models.Permission.Role import Role
from checkpoint.models.Permission.Domain import Domain
from checkpoint.models.Permission.IdentityGroup import IdentityGroup

from checkpoint.models.Permission.repository.Permission import Permission as Repository
from checkpoint.models.Permission.repository.PermissionPrivilege import PermissionPrivilege as PermissionPrivilegeRepository

from checkpoint.helpers.Exception import CustomException


class Permission:

    # IdentityGroupRoleDomain

    def __init__(self, permissionId: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id: int = int(permissionId)
        self.identityGroup: IdentityGroup
        self.role: Role
        self.domain: Domain

        self.__load()



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def delete(self) -> None:
        try:
            Repository.delete(self.id)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def hasUserPermission(groups: list, action: str, assetId: int = 0, domain: str = "") -> bool:
        # Authorizations' list allowed for any (authenticated) user.
        if action == "authorizations_get":
            return True

        # Superadmin's group.
        for gr in groups:
            if gr.lower() == "automation.local":
                return True

        try:
            return bool(
                PermissionPrivilegeRepository.countUserPermissions(groups, action, assetId, domain)
            )
        except Exception as e:
            raise e



    @staticmethod
    def permissionsDataList() -> list:

        #     {
        #         "id": 2,
        #         "identity_group_name": "groupAdmin",
        #         "identity_group_identifier": "cn=groupadmin,cn=users,dc=lab,dc=local",
        #         "role": "admin",
        #         "domain": {
        #             "asset_id": 1,
        #             "name": "any"
        #         }
        #     },

        try:
            return Repository.list()
        except Exception as e:
            raise e



    @staticmethod
    def authorizationsList(groups: list) -> dict:

        #     "assets_get": [
        #         {
        #             "assetId": "1",
        #             "domain": "any"
        #         }
        #     ],
        #     "domains_get": [
        #         {
        #             "assetId": "1",
        #             "domain": "any"
        #         }
        #     ],
        #     ...

        superadmin = False
        for gr in groups:
            if gr.lower() == "automation.local":
                superadmin = True
                break

        if superadmin:
            # Superadmin's permissions override.
            authorizations = {
                "any": [
                    {
                        "assetId": 0,
                        "domain": "any"
                    }
                ]
            }
        else:
            try:
                authorizations = PermissionPrivilegeRepository.authorizationsList(groups)
            except Exception as e:
                raise e

        return authorizations



    @staticmethod
    def addFacade(identityGroupIdentifier: str, role: str, domainInfo: dict) -> None:
        domainAssetId = domainInfo.get("assetId", "")
        domainName = domainInfo.get("name", "")

        try:
            # Get existent or new domain.
            if role == "admin":
                # Role admin -> "any" partition, which always exists.
                domain = Domain(assetId=domainAssetId, name="any")
            else:
                try:
                    # Try retrieving domain.
                    domain = Domain(assetId=domainAssetId, name=domainName)
                except CustomException as e:
                    if e.status == 404:
                        try:
                            # If domain does not exist, create it (permissions database).
                            domain = Domain(
                                id=Domain.add(domainAssetId, domainName)
                            )
                        except Exception:
                            raise e
                    else:
                        raise e

            Permission.__add(
                identityGroup=IdentityGroup(identityGroupIdentifier=identityGroupIdentifier),
                role=Role(role=role),
                domain=domain
            )
        except Exception as e:
            raise e



    @staticmethod
    def modifyFacade(permissionId: int, identityGroupIdentifier: str, role: str, domainInfo: dict) -> None:
        domainAssetId = domainInfo.get("assetId", "")
        domainName = domainInfo.get("name", "")

        try:
            # Get existent or new domain.
            if role == "admin":
                # role admin -> "any" partition, which always exists.
                domain = Domain(assetId=domainAssetId, name="any")
            else:
                try:
                    # Try retrieving domain.
                    domain = Domain(assetId=domainAssetId, name=domainName)
                except CustomException as e:
                    if e.status == 404:
                        try:
                            # If domain does not exist, create it (permissions database).
                            domain = Domain(
                                id=Domain.add(domainAssetId, domainName)
                            )
                        except Exception:
                            raise e
                    else:
                        raise e

            Permission(permissionId).__modify(
                identityGroup=IdentityGroup(identityGroupIdentifier=identityGroupIdentifier),
                role=Role(role=role),
                domain=domain
            )
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __load(self) -> None:
        try:
            info = Repository.get(self.id)

            self.identityGroup = IdentityGroup(id=info["id_group"])
            self.role = Role(id=info["id_role"])
            self.domain = Domain(id=info["id_domain"])
        except Exception as e:
            raise e



    def __modify(self, identityGroup: IdentityGroup, role: Role, domain: Domain) -> None:
        try:
            Repository.modify(
                self.id,
                identityGroupId=identityGroup.id,
                roleId=role.id,
                domainId=domain.id
            )
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private static methods
    ####################################################################################################################

    @staticmethod
    def __add(identityGroup: IdentityGroup, role: Role, domain: Domain) -> None:
        try:
            Repository.add(
                identityGroupId=identityGroup.id,
                roleId=role.id,
                domainId=domain.id
            )
        except Exception as e:
            raise e
