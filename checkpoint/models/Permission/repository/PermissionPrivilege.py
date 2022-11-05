from typing import List, Dict

from django.db import connection

from checkpoint.helpers.Exception import CustomException
from checkpoint.helpers.Database import Database as DBHelper


class PermissionPrivilege:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(filterGroups: list = None, showPrivileges: bool = False) -> list:
        # List identity groups with related information regarding the associated roles on domains,
        # and optionally detailed privileges' descriptions.
        filterGroups = filterGroups or []
        groupWhere = ""
        j = 0

        c = connection.cursor()

        try:
            # Build WHERE clause when filterGroups is specified.
            if filterGroups:
                groupWhere = "WHERE ("
                for _ in filterGroups:
                    groupWhere += "identity_group.identity_group_identifier = %s || "
                groupWhere = groupWhere[:-4] + ") "

            c.execute(
                "SELECT identity_group.*, " 

                "IFNULL(GROUP_CONCAT( "
                    "DISTINCT CONCAT(role.role,'::',CONCAT(domain.id_asset,'::',domain.domain)) " 
                    "ORDER BY role.id "
                    "SEPARATOR ',' "
                "), '') AS roles_domain, "

                "IFNULL(GROUP_CONCAT( "
                    "DISTINCT CONCAT(privilege.privilege,'::',domain.id_asset,'::',domain.domain,'::',privilege.privilege_type) " 
                    "ORDER BY privilege.id "
                    "SEPARATOR ',' "
                "), '') AS privileges_domain "

                "FROM identity_group "
                "LEFT JOIN group_role_domain ON group_role_domain.id_group = identity_group.id "
                "LEFT JOIN role ON role.id = group_role_domain.id_role "
                "LEFT JOIN `domain` ON `domain`.id = group_role_domain.id_domain "
                "LEFT JOIN role_privilege ON role_privilege.id_role = role.id "
                "LEFT JOIN privilege ON privilege.id = role_privilege.id_privilege "
                + groupWhere +
                "GROUP BY identity_group.id",
                      filterGroups
            )

            # Simple start query:
            # SELECT identity_group.*, role.role, privilege.privilege, `domain`.domain
            # FROM identity_group
            # LEFT JOIN group_role_domain ON group_role_domain.id_group = identity_group.id
            # LEFT JOIN role ON role.id = group_role_domain.id_role
            # LEFT JOIN `domain` ON `domain`.id = group_role_domain.id_domain
            # LEFT JOIN role_privilege ON role_privilege.id_role = role.id
            # LEFT JOIN privilege ON privilege.id = role_privilege.id_privilege
            # GROUP BY identity_group.id

            items: List[Dict] = DBHelper.asDict(c)

            # "items": [
            # ...,
            # {
            #    "id": 2,
            #    "name": "groupStaff",
            #    "identity_group_identifier": "cn=groupStaff,cn=users,dc=lab,dc=local",
            #    "roles_domain": "staff::1::Common",
            #    "privileges_domain": "certificates_post::1::Common::1::0,poolMember_get::1::Common::0::0,poolMember_patch::1::Common::0::0,poolMembers_get::1::Common::0::0,poolMemberStats_get::1::Common::0::0,pools_get::1::Common::0::0,domains_get::1::Common::1::1"
            # },
            # ...
            # ]

            for ln in items:
                if "roles_domain" in items[j]:
                    if "," in ln["roles_domain"]:
                        items[j]["roles_domain"] = ln["roles_domain"].split(",") # "staff::1::domain,...,readonly::2::domain" string to list value: replace into original data structure.
                    else:
                        items[j]["roles_domain"] = [ ln["roles_domain"] ] # simple string to list.

                    # "roles_domain": [
                    #    "admin::1::any",
                    #    "staff::1::PARTITION1",
                    #    "staff::2::PARTITION2"
                    # ]

                    rolesStructure = dict()
                    for rls in items[j]["roles_domain"]:
                        if "::" in rls:
                            rlsList = rls.split("::")
                            if not str(rlsList[0]) in rolesStructure:
                                # Initialize list if not already done.
                                rolesStructure[rlsList[0]] = list()

                            rolesStructure[rlsList[0]].append({
                                "assetId": rlsList[1],
                                "domain": rlsList[2]
                            })

                    items[j]["roles_domain"] = rolesStructure

                    #"roles_domain": {
                    #    "staff": [
                    #        {
                    #            "assetId": 1
                    #            "domain": "PARTITION1"
                    #        },
                    #        {
                    #            "assetId": 2
                    #            "domain": "PARTITION2"
                    #        },
                    #    ],
                    #    "admin": [
                    #        {
                    #            "assetId": 1
                    #            "domain": "any"
                    #        },
                    #    ]
                    #}

                if showPrivileges:
                    # Add detailed privileges' descriptions to the output.
                    if "privileges_domain" in items[j]:
                        if "," in ln["privileges_domain"]:
                            items[j]["privileges_domain"] = ln["privileges_domain"].split(",")
                        else:
                            items[j]["privileges_domain"] = [ ln["privileges_domain"] ]

                        ppStructure = dict()
                        for pls in items[j]["privileges_domain"]:
                            if "::" in pls:
                                pList = pls.split("::")
                                if not str(pList[0]) in ppStructure:
                                    ppStructure[pList[0]] = list()

                                # Differentiate permission type:
                                # global:
                                #     a privilege does not require the asset to be specified <--> it's valid for all assets;
                                #     set "any" for assets value.

                                # asset:
                                #    a privilege does not require the partitions to be specified <--> it's valid for all partitions within the asset;
                                #    set "any" for partitions value.
                                #
                                # object:
                                #     standard.

                                if pList[3]:
                                    if pList[3] == "global":
                                        pList[1] = 0
                                        pList[2] = "any"
                                    if pList[3] == "asset":
                                        pList[2] = "any"

                                if not any(v['assetId'] == 0 for v in ppStructure[pList[0]]): # insert value only if not already present (applied to assetId "0").
                                    ppStructure[pList[0]].append({
                                        "assetId": pList[1],
                                        "domain": pList[2],
                                    })

                        items[j]["privileges_domain"] = ppStructure
                else:
                    del items[j]["privileges_domain"]

                j = j+1

            return items
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def authorizationsList(groups: list) -> dict:
        permissions = list()
        combinedPermissions = dict()

        try:
            o = PermissionPrivilege.list(filterGroups=groups, showPrivileges=True)

            # [
            #   {
            #     "id": 3,
            #     "name": "groupStaff",
            #     "identity_group_identifier": "cn=groupstaff,cn=users,dc=lab,dc=local",
            #     "roles_domain": { ... },
            #     "privileges_domain": { ... }
            #   },
            #   ...
            # ]

            # Collect every permission related to the group in groups.
            for identityGroup in groups:
                for el in o:
                    if "identity_group_identifier" in el:
                        if el["identity_group_identifier"].lower() == identityGroup.lower():
                            permissions.append(el["privileges_domain"])

            # [
            #    {
            #        "assets_get": [
            #            {
            #                "assetId": "1",
            #                "domain": "any"
            #            }
            #        ],
            #        ...
            #    },
            #    {
            #        "assets_get": [
            #            {
            #                "assetId": "1",
            #                "domain": "Common"
            #            }
            #        ],
            #        ...
            #    }
            # ]

            # Clean up structure.
            for el in permissions:
                for k, v in el.items():

                    # Initialize list if not already done.
                    if not str(k) in combinedPermissions:
                        combinedPermissions[k] = list()

                    for innerEl in v:
                        if innerEl not in combinedPermissions[k]:
                            combinedPermissions[k].append(innerEl)

            # {
            #    ...
            #    "assets_get": [
            #        {
            #            "assetId": "1",
            #            "domain": "any"
            #        },
            #        {
            #            "assetId": "1",
            #            "domain": "Common"
            #        },
            #        {
            #            "assetId": "2",
            #            "domain": "Common"
            #        }
            #    ],
            #    ...
            # }

            # Clean up structure.
            for k, v in combinedPermissions.items():
                asset = 0
                for el in v:
                    if el["domain"] == "any":
                        asset = el["assetId"] # assetId for domain "any".

                if asset:
                    for j in range(len(v)):
                        try:
                            if v[j]["assetId"] == asset and v[j]["domain"] != "any":
                                del v[j]
                        except Exception:
                            pass

            # {
            #    ...
            #    "assets_get": [
            #        {
            #            "assetId": "1",
            #            "domain": "any"
            #        },
            #        {
            #            "assetId": "2",
            #            "domain": "Common"
            #        }
            #    ],
            #    ...
            # }
        except Exception as e:
            raise e

        return combinedPermissions



    @staticmethod
    def countUserPermissions(groups: list, action: str, assetId: int = 0, domainName: str = "") -> int:
        if action and groups:
            assetWhere = ""
            domainWhere = ""

            c = connection.cursor()

            try:
                # Build the first half of the where condition of the query.
                # Obtain: WHERE (identity_group.identity_group_identifier = %s || identity_group.identity_group_identifier = %s || identity_group.identity_group_identifier = %s || ....)
                args = groups.copy()
                groupWhere = ""
                for g in groups:
                    groupWhere += "identity_group.identity_group_identifier = %s || "

                # Put all the args of the query in a list.
                if assetId:
                    args.append(assetId)
                    assetWhere = "AND `domain`.id_asset = %s "

                if domainName:
                    args.append(domainName)
                    domainWhere = "AND (`domain`.`domain` = %s OR `domain`.`domain` = 'any') " # if "any" appears in the query results so far -> pass.

                args.append(action)

                c.execute(
                    "SELECT COUNT(*) AS count "
                    "FROM identity_group "
                    "LEFT JOIN group_role_domain ON group_role_domain.id_group = identity_group.id "
                    "LEFT JOIN role ON role.id = group_role_domain.id_role "
                    "LEFT JOIN role_privilege ON role_privilege.id_role = role.id "
                    "LEFT JOIN `domain` ON `domain`.id = group_role_domain.id_domain "                      
                    "LEFT JOIN privilege ON privilege.id = role_privilege.id_privilege "
                    "WHERE (" + groupWhere[:-4] + ") " +
                    assetWhere +
                    domainWhere +
                    "AND privilege.privilege = %s ",
                        args
                )

                return DBHelper.asDict(c)[0]["count"]
            except Exception as e:
                raise CustomException(status=400, payload={"database": e.__str__()})
            finally:
                c.close()

        return 0
