from checkpoint.models.CheckPoint.Role import Role
from checkpoint.models.CheckPoint.Rule import Rule

from checkpoint.helpers.Exception import CustomException
from checkpoint.helpers.Log import Log


class VpnToServices:
    def __init__(self, sessionId: str, assetId: int, domain: str, name: str, user: str, workflowId: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sessionId = sessionId
        self.assetId: int = int(assetId)
        self.domain: str = domain
        self.name: str = name
        self.username = user
        self.workflowId = workflowId



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def __call__(self, *args, **kwargs) -> list:
        try:
            services = list()
            rules = list()

            roleInformation = Role.searchByName(self.sessionId, self.assetId, self.domain, self.name, localOnly=False)
            if roleInformation and "uid" in roleInformation:
                role = Role(self.sessionId, self.assetId, self.domain, uid=roleInformation["uid"])
                w = role.whereUsed(indirect=True)

                for j in ("used-directly", "used-indirectly"):
                    rules.extend(w[j].get("access-control-rules", []))

                # Get roles from security rules.
                for rule in rules:
                    if "layer" in rule and "rule" in rule:
                        ruleAcl = Rule(self.sessionId, "access", self.assetId, self.domain, layerUid=rule["layer"].get("uid", ""), uid=rule["rule"].get("uid", "")).info()
                        if "destination" in ruleAcl:
                            for j in ruleAcl["destination"]:
                                if "uid" in j and "name" in j and "type" in j:
                                    services.append({
                                        "uid": j["uid"],
                                        "name": j["name"],
                                        "type": j["type"],
                                    })
            else:
                raise CustomException(status=404, payload={"CheckPoint": "role not found"})

            return services
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def usedModels() -> list:
        return ["object", "host", "ruleaccess", "roleaccess"]
