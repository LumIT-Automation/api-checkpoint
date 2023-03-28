from django.urls import path

from .controllers import Root
from .controllers.CheckPoint.Asset import Asset, Assets
from .controllers.CheckPoint import CheckPointGateways
from .controllers.Permission import Authorizations, IdentityGroups, IdentityGroup, Roles, Permission, Permissions
from .controllers.CheckPoint import Domain, Domains
from .controllers.CheckPoint import Sessions
from .controllers.CheckPoint import Object, ObjectUsed, ObjectsUnused
from .controllers.CheckPoint import Network, Networks
from .controllers.CheckPoint import AddressRanges, AddressRange
from .controllers.CheckPoint import DatacenterServers, DatacenterServer
from .controllers.CheckPoint import DatacenterQueries, DatacenterQuery
from .controllers.CheckPoint import Tasks, Task
from .controllers.CheckPoint import Host, Hosts
from .controllers.CheckPoint.UseCases import RemoveHost, VpnToHost, VpnToServices
from .controllers.CheckPoint import Group, Groups
from .controllers.CheckPoint import GroupHosts, GroupHost
from .controllers.CheckPoint import GroupGroups, GroupFatherGroups, GroupGroup
from .controllers.CheckPoint import GroupNetworks, GroupNetwork
from .controllers.CheckPoint import GroupAddressRanges, GroupAddressRange
from .controllers.CheckPoint import ServicesTcp, ServiceTcp
from .controllers.CheckPoint import ServicesUdp, ServiceUdp
from .controllers.CheckPoint import ApplicationSites, ApplicationSite
from .controllers.CheckPoint import ApplicationSiteCategories, ApplicationSiteCategory
from .controllers.CheckPoint import PolicyPackages, PolicyPackage
from .controllers.CheckPoint import RuleAccess, RuleThreat, RuleHttps
from .controllers.CheckPoint import RulebaseAccess, RulebaseThreat, RulebaseHttps
from .controllers.CheckPoint import RuleObjectsAccess, RuleObjectsThreat, RuleObjectsHttps, RuleObjectAccess, RuleObjectThreat, RuleObjectHttps
from .controllers.CheckPoint import NatRule, NatRulebase
from .controllers.CheckPoint import NatRuleObjects
from .controllers.CheckPoint import Roles as CheckPointRoles, Role as CheckPointRole
from .controllers.CheckPoint import LayersAccess, LayersThreat, LayersHttps, LayerAccess, LayerThreat, LayerHttps
from .controllers.CheckPoint import Ips, IpsAttributes, IpsAttribute, IpsSchedule
from .controllers.CheckPoint import User
from .controllers.Configuration import Configuration
from .controllers.History import History


urlpatterns = [
    path('', Root.RootController.as_view()),

    path('identity-groups/', IdentityGroups.PermissionIdentityGroupsController.as_view(), name='permission-identity-groups'),
    path('identity-group/<str:identityGroupIdentifier>/', IdentityGroup.PermissionIdentityGroupController.as_view(), name='permission-identity-group'),
    path('roles/', Roles.PermissionRolesController.as_view(), name='permission-roles'),
    path('permissions/', Permissions.PermissionsController.as_view(), name='permissions'),
    path('permission/<int:permissionId>/', Permission.PermissionController.as_view(), name='permission'),

    path('authorizations/', Authorizations.AuthorizationsController.as_view(), name='authorizations'),

    path('configuration/<str:configType>/', Configuration.ConfigurationController.as_view(), name='configuration'),

    # Asset.
    path('assets/', Assets.CheckPointAssetsController.as_view(), name='checkpoint-assets'),
    path('asset/<int:assetId>/', Asset.CheckPointAssetController.as_view(), name='checkpoint-asset'),

    # CheckPoint gateways.
    path('<int:assetId>/gateways/', CheckPointGateways.CheckPointGatewaysController.as_view(), name='checkpoint-gateways'),

    # Domains.
    path('<int:assetId>/domains/', Domains.CheckPointDomainsController.as_view(), name='domains'),
    path('<int:assetId>/domain/<str:domainUid>/', Domain.CheckPointDomainController.as_view(), name='domain'),

    # Sessions.
    path('<int:assetId>/sessions/', Sessions.CheckPointSessionsController.as_view(), name='sessions-mds'),
    path('<int:assetId>/<str:domain>/sessions/', Sessions.CheckPointSessionsController.as_view(), name='sessions'),

    # Objects.
    path('<int:assetId>/<str:domain>/object/<str:objectUid>/', Object.CheckPointObjectController.as_view(), name='object'),
    path('<int:assetId>/<str:domain>/object/<str:objectUid>/where-used/', ObjectUsed.CheckPointObjectWhereUsedController.as_view(), name='object-where-used'),
    path('<int:assetId>/<str:domain>/objects/unused/', ObjectsUnused.CheckPointObjectsUnusedController.as_view(), name='objects-unused'),

    # Networks.
    path('<int:assetId>/<str:domain>/networks/', Networks.CheckPointNetworksController.as_view(), name='networks'),
    path('<int:assetId>/<str:domain>/network/<str:networkUid>/', Network.CheckPointNetworkController.as_view(), name='network'),

    # Address ranges.
    path('<int:assetId>/<str:domain>/address-ranges/', AddressRanges.CheckPointAddressRangesController.as_view(), name='address-ranges'),
    path('<int:assetId>/<str:domain>/address-range/<str:rangeUid>/', AddressRange.CheckPointAddressRangeController.as_view(), name='address-range'),

    # Hosts.
    path('<int:assetId>/<str:domain>/hosts/', Hosts.CheckPointHostsController.as_view(), name='hosts'),
    path('<int:assetId>/<str:domain>/host/<str:hostUid>/', Host.CheckPointHostController.as_view(), name='host'),

    # Groups.
    path('<int:assetId>/<str:domain>/groups/', Groups.CheckPointGroupsController.as_view(), name='groups'),
    path('<int:assetId>/<str:domain>/group/<str:groupUid>/', Group.CheckPointGroupController.as_view(), name='group'),

    # GroupHosts.
    path('<int:assetId>/<str:domain>/group/<str:groupUid>/hosts/', GroupHosts.CheckPointGroupHostsController.as_view(), name='group-hosts'),
    path('<int:assetId>/<str:domain>/group/<str:groupUid>/host/<str:hostUid>/', GroupHost.CheckPointGroupHostController.as_view(), name='group-host'),

    # GroupGroups.
    path('<int:assetId>/<str:domain>/group/<str:groupUid>/groups/', GroupGroups.CheckPointGroupGroupsController.as_view(), name='group-groups'),
    path('<int:assetId>/<str:domain>/group/<str:groupUid>/group/<str:childGroupUid>/', GroupGroup.CheckPointGroupGroupController.as_view(), name='group-group'),

    path('<int:assetId>/<str:domain>/group/<str:groupUid>/father-groups/', GroupFatherGroups.CheckPointGroupFatherGroupsController.as_view(), name='group-father-groups'),

    # GroupNetworks.
    path('<int:assetId>/<str:domain>/group/<str:groupUid>/networks/', GroupNetworks.CheckPointGroupNetworksController.as_view(), name='group-networks'),
    path('<int:assetId>/<str:domain>/group/<str:groupUid>/network/<str:networkUid>/', GroupNetwork.CheckPointGroupNetworkController.as_view(), name='group-network'),

    # GroupAddressRanges.
    path('<int:assetId>/<str:domain>/group/<str:groupUid>/address-ranges/', GroupAddressRanges.CheckPointGroupAddressRangesController.as_view(), name='group-address-ranges'),
    path('<int:assetId>/<str:domain>/group/<str:groupUid>/address-range/<str:rangeUid>/', GroupAddressRange.CheckPointGroupAddressRangeController.as_view(), name='group-address-range'),

    # Services tcp.
    path('<int:assetId>/<str:domain>/services-tcp/', ServicesTcp.CheckPointServicesTcpController.as_view(), name='services-tcp'),
    path('<int:assetId>/<str:domain>/service-tcp/<str:serviceUid>/', ServiceTcp.CheckPointServiceTcpController.as_view(), name='service-tcp'),

    # Services udp.
    path('<int:assetId>/<str:domain>/services-udp/', ServicesUdp.CheckPointServicesUdpController.as_view(), name='services-udp'),
    path('<int:assetId>/<str:domain>/service-udp/<str:serviceUid>/', ServiceUdp.CheckPointServiceUdpController.as_view(), name='service-udp'),

    # Datacenter servers.
    path('<int:assetId>/<str:domain>/datacenter-servers/', DatacenterServers.CheckPointDatacenterServersController.as_view(), name='datacenter-servers'),
    path('<int:assetId>/<str:domain>/datacenter-server/<str:datacenterUid>/', DatacenterServer.CheckPointDatacenterServerController.as_view(), name='datacenter-server'),

    # Datacenter queries.
    path('<int:assetId>/<str:domain>/datacenter-queries/', DatacenterQueries.CheckPointDatacenterQueriesController.as_view(), name='datacenter-queries'),
    path('<int:assetId>/<str:domain>/datacenter-query/<str:datacenterUid>/', DatacenterQuery.CheckPointDatacenterQueryController.as_view(), name='datacenter-query'),

    # Tasks.
    path('<int:assetId>/<str:domain>/tasks/', Tasks.CheckPointTasksController.as_view(), name='taks'),
    path('<int:assetId>/<str:domain>/task/<str:taskUid>/', Task.CheckPointTaskController.as_view(), name='task'),

    # Application sites.
    path('<int:assetId>/<str:domain>/application-sites/', ApplicationSites.CheckPointApplicationSitesController.as_view(), name='application-sites'),
    path('<int:assetId>/<str:domain>/application-site/<str:appSiteUid>/', ApplicationSite.CheckPointApplicationSiteController.as_view(), name='application-site'),

    # Application site categories.
    path('<int:assetId>/<str:domain>/application-site-categories/', ApplicationSiteCategories.CheckPointApplicationSiteCategoriesController.as_view(), name='application-site-categories'),
    path('<int:assetId>/<str:domain>/application-site-category/<str:categoryUid>/', ApplicationSiteCategory.CheckPointApplicationSiteCategoryController.as_view(), name='application-site-category'),

    # Policy packages.
    path('<int:assetId>/<str:domain>/policy-packages/', PolicyPackages.CheckPointPolicyPackagesController.as_view(), name='policy-packages'),
    path('<int:assetId>/<str:domain>/policy-package/<str:packageUid>/', PolicyPackage.CheckPointPolicyPackageController.as_view(), name='policy-package'),

    # NAT rulebase.
    path('<int:assetId>/<str:domain>/package/<str:packageUid>/nat-rules/', NatRulebase.CheckPointNatRulebaseController.as_view(), name='nat-rulebase-in-a-policy-package'),

    # NAT rule.
    path('<int:assetId>/<str:domain>/package/<str:packageUid>/nat-rule/<str:natRuleUid>/', NatRule.CheckPointNatRuleController.as_view(), name='nat-rule'),

    # NAT rule objects.
    path('<int:assetId>/<str:domain>/package/<str:packageUid>/nat-rule/<str:natRuleUid>/objects/', NatRuleObjects.CheckPointNatRuleObjectsController.as_view(), name='objects-in-nat-rule'),

    # Layers.
    path('<int:assetId>/<str:domain>/access-layers/', LayersAccess.CheckPointAccessLayersController.as_view(), name='access-layers'),
    path('<int:assetId>/<str:domain>/threat-layers/', LayersThreat.CheckPointThreatLayersController.as_view(), name='threat-layers'),
    path('<int:assetId>/<str:domain>/https-layers/', LayersHttps.CheckPointHttpsLayersController.as_view(), name='https-layers'),

    path('<int:assetId>/<str:domain>/access-layer/<str:layerUid>/', LayerAccess.CheckPointAccessLayerController.as_view(), name='access-layer'),
    path('<int:assetId>/<str:domain>/threat-layer/<str:layerUid>/', LayerThreat.CheckPointThreatLayerController.as_view(), name='threat-layer'),
    path('<int:assetId>/<str:domain>/https-layer/<str:layerUid>/', LayerHttps.CheckPointHttpsLayerController.as_view(), name='https-layer'),

    # Rules (Rulebase).
    path('<int:assetId>/<str:domain>/access-layer/<str:layerUid>/rules/', RulebaseAccess.CheckPointAccessRulebaseController.as_view(), name='rulebase-in-an-access-layer'),
    path('<int:assetId>/<str:domain>/threat-layer/<str:layerUid>/rules/', RulebaseThreat.CheckPointThreatRulebaseController.as_view(), name='rulebase-in-a-threat-layer'),
    path('<int:assetId>/<str:domain>/https-layer/<str:layerUid>/rules/', RulebaseHttps.CheckPointHttpsRulebaseController.as_view(), name='rulebase-in-a-https-layer'),

    # Rule.
    path('<int:assetId>/<str:domain>/layer/<str:layerUid>/access-rule/<str:ruleUid>/', RuleAccess.CheckPointAccessLayerController.as_view(), name='access-rule'),
    path('<int:assetId>/<str:domain>/layer/<str:layerUid>/threat-rule/<str:ruleUid>/', RuleThreat.CheckPointThreatLayerController.as_view(), name='threat-rule'),
    path('<int:assetId>/<str:domain>/layer/<str:layerUid>/https-rule/<str:ruleUid>/', RuleHttps.CheckPointHttpsLayerController.as_view(), name='https-rule'),

    # Rule objects.
    path('<int:assetId>/<str:domain>/layer/<str:layerUid>/access-rule/<str:ruleUid>/objects/', RuleObjectsAccess.CheckPointAccessRuleObjectsController.as_view(), name='objects-in-access-rule'),
    path('<int:assetId>/<str:domain>/layer/<str:layerUid>/threat-rule/<str:ruleUid>/objects/', RuleObjectsThreat.CheckPointThreatRuleObjectsController.as_view(), name='objects-in-threat-rule'),
    path('<int:assetId>/<str:domain>/layer/<str:layerUid>/https-rule/<str:ruleUid>/objects/', RuleObjectsHttps.CheckPointHttpsRuleObjectsController.as_view(), name='objects-in-https-rule'),

    path('<int:assetId>/<str:domain>/layer/<str:layerUid>/access-rule/<str:ruleUid>/object/<str:ruleObjectUid>/', RuleObjectAccess.CheckPointAccessRuleObjectController.as_view(), name='object-in-access-rule'),
    path('<int:assetId>/<str:domain>/layer/<str:layerUid>/threat-rule/<str:ruleUid>/object/<str:ruleObjectUid>/', RuleObjectThreat.CheckPointThreatRuleObjectController.as_view(), name='object-in-threat-rule'),
    path('<int:assetId>/<str:domain>/layer/<str:layerUid>/https-rule/<str:ruleUid>/object/<str:ruleObjectUid>/', RuleObjectHttps.CheckPointHttpsRuleObjectController.as_view(), name='object-in-https-rule'),

    # Roles.
    path('<int:assetId>/<str:domain>/access-roles/', CheckPointRoles.CheckPointRolesController.as_view(), name='access-roles'),
    path('<int:assetId>/<str:domain>/access-role/<str:roleUid>/', CheckPointRole.CheckPointRoleController.as_view(), name='access-role'),

    # Ips.
    path('<int:assetId>/<str:domain>/ips/', Ips.CheckPointIpsController.as_view(), name='ips'),
    path('<int:assetId>/<str:domain>/ips-extended-attributes/', IpsAttributes.CheckPointIpsExtendedAttributesController.as_view(), name='ips-extended-attributes'),
    path('<int:assetId>/<str:domain>/ips-extended-attribute/<str:attributeUid>/', IpsAttribute.CheckPointIpsExtendedAttributeController.as_view(), name='ips-extended-attributes'),

    path('<int:assetId>/<str:domain>/ips-schedule/', IpsSchedule.CheckPointIpsScheduleController.as_view(), name='ips-schedule'),

    # Users.
    path('<int:assetId>/<str:domain>/user/<str:userUid>/', User.CheckPointUserController.as_view(), name='user'),

    # Use cases.
    path('<int:assetId>/remove-host/', RemoveHost.CheckPointRemoveHostController.as_view(), name='remove-host'), # completely remove host and related.
    path('<int:assetId>/<str:domain>/vpn-to-host/', VpnToHost.CheckPointVpnProfilesToHostController.as_view(), name='vpn-to-host'), # which vpn profiles (roles) reach the host.
    path('<int:assetId>/<str:domain>/vpn-to-services/', VpnToServices.CheckPointVpnProfileToServicesController.as_view(), name='vpn-to-host'), # services reached by a vpn profile (role).

    # Log history.
    path('history/', History.HistoryLogsController.as_view(), name='checkpoint-log-history'),
]
