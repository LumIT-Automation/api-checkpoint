from rest_framework import serializers
from checkpoint.models.Permission.Privilege import Privilege
from checkpoint.models.Permission.Role import Role


class IdentityGroupsAssestRolesSubItems(serializers.Serializer):
    assetId = serializers.IntegerField(required=True)
    domain = serializers.CharField(max_length=64, required=True)

class IdentityGroupsAssestRolesItems(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Adding dynamic fields as taken from the Roles model.
        additionalFields = []
        r = Role.dataList()
        for additionalField in r:
            if "role" in additionalField:
                additionalFields.append(additionalField["role"])

        for af in additionalFields:
            self.fields[af] = IdentityGroupsAssestRolesSubItems(many=True, required=False)

class IdentityGroupsAssestPrivilegeItems(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Adding dynamic fields as taken from the Privilege model.
        additionalFields = []
        r = Privilege.dataList()
        for additionalField in r:
            if "privilege" in additionalField:
                additionalFields.append(additionalField["privilege"])

        for af in additionalFields:
            self.fields[af] = IdentityGroupsAssestRolesSubItems(many=True, required=False)

class IdentityGroupSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=64, required=True)
    identity_group_identifier = serializers.CharField(max_length=255, required=True)

    roles_domain = IdentityGroupsAssestRolesItems(required=False)
    privileges_domain = IdentityGroupsAssestPrivilegeItems(required=False)
