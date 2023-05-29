from django.db import connection

from checkpoint.helpers.Exception import CustomException
from checkpoint.helpers.Database import Database as DBHelper


class Permission:

    # IdentityGroupRoleDomain

    # Tables: group_role_domain, identity_group, role, domain



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def get(permissionId: int) -> dict:
        c = connection.cursor()

        try:
            c.execute("SELECT * FROM group_role_domain WHERE id=%s", [permissionId])

            return DBHelper.asDict(c)[0]
        except IndexError:
            raise CustomException(status=404, payload={"database": "non existent permission"})
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def modify(permissionId: int, identityGroupId: int, roleId: int, domainId: int) -> None:
        c = connection.cursor()

        try:
            c.execute("UPDATE group_role_domain SET id_group=%s, id_role=%s, id_domain=%s WHERE id=%s", [
                identityGroupId, # AD or RADIUS group.
                roleId,
                domainId,
                permissionId
            ])
        except Exception as e:
            if e.__class__.__name__ == "IntegrityError" \
                    and e.args and e.args[0] and e.args[0] == 1062:
                        raise CustomException(status=400, payload={"database": "duplicated entry"})
            else:
                raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def delete(permissionId: int) -> None:
        c = connection.cursor()

        try:
            c.execute("DELETE FROM group_role_domain WHERE id = %s", [permissionId])
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def list() -> list:
        c = connection.cursor()

        try:
            c.execute(
                "SELECT "
                    "group_role_domain.id, "
                    "identity_group.name AS identity_group_name, "
                    "identity_group.identity_group_identifier AS identity_group_identifier, "
                    "role.role AS role, "
                    "`domain`.id_asset AS domain_asset, "
                    "`domain`.`domain` AS domain_name "
                "FROM identity_group "
                "LEFT JOIN group_role_domain ON group_role_domain.id_group = identity_group.id "
                "LEFT JOIN role ON role.id = group_role_domain.id_role "
                "LEFT JOIN `domain` ON `domain`.id = group_role_domain.id_domain "
                "WHERE role.role IS NOT NULL")
            l = DBHelper.asDict(c)

            for el in l:
                el["domain"] = {
                    "id_asset": el["domain_asset"],
                    "name": el["domain_name"]
                }

                del(el["domain_asset"])
                del(el["domain_name"])

            return l
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def add(identityGroupId: int, roleId: int, domainId: int) -> None:
        c = connection.cursor()

        try:
            c.execute("INSERT INTO group_role_domain (id_group, id_role, id_domain) VALUES (%s, %s, %s)", [
                identityGroupId, # AD or RADIUS group.
                roleId,
                domainId
            ])
        except Exception as e:
            if e.__class__.__name__ == "IntegrityError" \
                    and e.args and e.args[0] and e.args[0] == 1062:
                        raise CustomException(status=400, payload={"database": "duplicated entry"})
            else:
                raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()
