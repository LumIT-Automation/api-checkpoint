-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Creato il: Mag 06, 2021 alle 16:58
-- Versione del server: 10.3.27-MariaDB-0+deb10u1-log
-- Versione PHP: 7.3.27-1~deb10u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `api`
--

--
-- Dump dei dati per la tabella `configuration`
--

INSERT INTO `configuration` (`id`, `config_type`) VALUES
(1, 'global');

--
-- Dump dei dati per la tabella `privilege`
--

INSERT INTO `privilege` (`id`, `privilege`, `privilege_type`, `description`) VALUES
(1, 'asset_patch', 'asset', NULL),
(2, 'asset_delete', 'asset', NULL),
(3, 'assets_get', 'asset', NULL),
(4, 'assets_post', 'asset', NULL),
(5, 'permission_identityGroups_get', 'global', NULL),
(6, 'permission_identityGroups_post', 'global', NULL),
(7, 'permission_roles_get', 'global', NULL),
(8, 'permission_identityGroup_patch', 'global', NULL),
(9, 'permission_identityGroup_delete', 'global', NULL),
(10, 'domains_get', 'asset', NULL),
(11, 'domain_get', 'object', NULL),
(12, 'hosts_get', 'object', NULL),
(13, 'hosts_post', 'object', NULL),
(14, 'host_get', 'object', NULL),
(15, 'host_delete', 'object', NULL),
(16, 'host_patch', 'object', NULL),
(17, 'groups_get', 'object', NULL),
(18, 'groups_post', 'object', NULL),
(19, 'group_get', 'object', NULL),
(20, 'group_delete', 'object', NULL),
(21, 'group_patch', 'object', NULL),
(22, 'group_networks_get', 'object', NULL),
(23, 'group_networks_post', 'object', NULL),
(24, 'group_network_delete', 'object', NULL),
(25, 'group_hosts_get', 'object', NULL),
(26, 'group_hosts_post', 'object', NULL),
(27, 'group_host_delete', 'object', NULL),
(28, 'group_address_ranges_get', 'object', NULL),
(29, 'group_address_ranges_post', 'object', NULL),
(30, 'group_address_range_delete', 'object', NULL),
(31, 'application_sites_get', 'object', NULL),
(32, 'application_sites_post', 'object', NULL),
(33, 'application_site_category_get', 'object', NULL),
(34, 'application_site_category_delete', 'object', NULL),
(35, 'application_site_category_patch', 'object', NULL),
(36, 'application_site_categories_get', 'object', NULL),
(37, 'application_site_categories_post', 'object', NULL),
(38, 'application_site_get', 'object', NULL),
(39, 'application_site_delete', 'object', NULL),
(40, 'application_site_patch', 'object', NULL),
(41, 'address_ranges_get', 'object', NULL),
(42, 'address_ranges_post', 'object', NULL),
(43, 'address_range_get', 'object', NULL),
(44, 'address_range_delete', 'object', NULL),
(45, 'address_range_patch', 'object', NULL),
(46, 'networks_get', 'object', NULL),
(47, 'networks_post', 'object', NULL),
(48, 'network_get', 'object', NULL),
(49, 'network_delete', 'object', NULL),
(50, 'network_patch', 'object', NULL),
(51, 'nat_rulebase_get', 'object', NULL),
(52, 'nat_rulebase_post', 'object', NULL),
(53, 'nat_rule_get', 'object', NULL),
(54, 'nat_rule_delete', 'object', NULL),
(55, 'layers_get', 'object', NULL),
(56, 'layers_post', 'object', NULL),
(57, 'layer_get', 'object', NULL),
(58, 'layer_delete', 'object', NULL),
(59, 'layer_patch', 'object', NULL),
(60, 'services_get', 'object', NULL),
(61, 'services_post', 'object', NULL),
(62, 'service_get', 'object', NULL),
(63, 'service_delete', 'object', NULL),
(64, 'service_patch', 'object', NULL),
(65, 'rule_objects_get', 'object', NULL),
(66, 'rule_objects_post', 'object', NULL),
(67, 'rule_object_delete', 'object', NULL),
(68, 'rulebases_get', 'object', NULL),
(69, 'rulebases_post', 'object', NULL),
(70, 'rule_get', 'object', NULL),
(71, 'rule_delete', 'object', NULL),
(72, 'rule_patch', 'object', NULL),
(73, 'policy_packages_get', 'object', NULL),
(74, 'policy_packages_post', 'object', NULL),
(75, 'policy_package_get', 'object', NULL),
(76, 'policy_package_delete', 'object', NULL),
(77, 'policy_package_patch', 'object', NULL),
(78, 'objects_get', 'object', NULL),
(79, 'object_get', 'object', NULL),
(80, 'host_remove', 'asset', NULL),
(81, 'roles_get', 'object', NULL),
(82, 'role_get', 'object', NULL),
(83, 'checkpoint_gateways_get', 'object', NULL),
(84, 'vpn_to_host', 'asset', NULL),
(85, 'vpn_to_services', 'asset', NULL),
(86, 'datacenter_servers_get', 'object', NULL),
(87, 'datacenter_servers_post', 'object', NULL),
(88, 'datacenter_server_get', 'object', NULL),
(89, 'datacenter_server_delete', 'object', NULL),
(90, 'datacenter_server_patch', 'object', NULL),
(91, 'datacenter_queries_get', 'object', NULL),
(92, 'datacenter_queries_post', 'object', NULL),
(93, 'datacenter_query_get', 'object', NULL),
(94, 'datacenter_query_delete', 'object', NULL),
(95, 'datacenter_query_patch', 'object', NULL),
(96, 'configuration_put', 'global', NULL);

--
-- Dump dei dati per la tabella `role`
--

INSERT INTO `role` (`id`, `role`, `description`) VALUES
(1, 'admin', 'admin'),
(2, 'staff', 'read / write, excluding assets'),
(3, 'readonly', 'readonly'),
(4, 'workflow', 'workflow system user');

--
-- Dump dei dati per la tabella `role_privilege`
--

INSERT INTO `role_privilege` (`id_role`, `id_privilege`) VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(1, 5),
(1, 6),
(1, 7),
(1, 8),
(1, 9),
(1, 10),
(1, 11),
(1, 12),
(1, 13),
(1, 14),
(1, 15),
(1, 16),
(1, 17),
(1, 18),
(1, 19),
(1, 20),
(1, 21),
(1, 22),
(1, 23),
(1, 24),
(1, 25),
(1, 26),
(1, 27),
(1, 28),
(1, 29),
(1, 30),
(1, 31),
(1, 32),
(1, 33),
(1, 34),
(1, 35),
(1, 36),
(1, 37),
(1, 38),
(1, 39),
(1, 40),
(1, 41),
(1, 42),
(1, 43),
(1, 44),
(1, 45),
(1, 46),
(1, 47),
(1, 48),
(1, 49),
(1, 50),
(1, 51),
(1, 52),
(1, 53),
(1, 54),
(1, 55),
(1, 56),
(1, 57),
(1, 58),
(1, 59),
(1, 60),
(1, 61),
(1, 62),
(1, 63),
(1, 64),
(1, 65),
(1, 66),
(1, 67),
(1, 68),
(1, 69),
(1, 70),
(1, 71),
(1, 72),
(1, 73),
(1, 74),
(1, 75),
(1, 76),
(1, 77),
(1, 78),
(1, 79),
(1, 81),
(1, 82),
(1, 83),
(1, 84),
(1, 85),
(1, 86),
(1, 87),
(1, 88),
(1, 89),
(1, 90),
(1, 91),
(1, 92),
(1, 93),
(1, 94),
(1, 95),
(1, 96),
(2, 3),
(2, 10),
(2, 11),
(2, 12),
(2, 14),
(2, 17),
(2, 18),
(2, 19),
(2, 20),
(2, 21),
(2, 22),
(2, 23),
(2, 24),
(2, 25),
(2, 26),
(2, 27),
(2, 28),
(2, 29),
(2, 30),
(2, 31),
(2, 32),
(2, 33),
(2, 34),
(2, 35),
(2, 36),
(2, 37),
(2, 38),
(2, 39),
(2, 40),
(2, 41),
(2, 42),
(2, 43),
(2, 44),
(2, 45),
(2, 46),
(2, 47),
(2, 48),
(2, 49),
(2, 50),
(2, 51),
(2, 52),
(2, 53),
(2, 54),
(2, 55),
(2, 56),
(2, 57),
(2, 58),
(2, 59),
(2, 60),
(2, 61),
(2, 62),
(2, 63),
(2, 64),
(2, 65),
(2, 66),
(2, 67),
(2, 68),
(2, 69),
(2, 70),
(2, 71),
(2, 72),
(2, 73),
(2, 74),
(2, 75),
(2, 76),
(2, 77),
(2, 78),
(2, 79),
(2, 81),
(2, 82),
(2, 83),
(2, 84),
(2, 85),
(2, 86),
(2, 87),
(2, 88),
(2, 89),
(2, 90),
(2, 91),
(2, 92),
(2, 93),
(2, 94),
(2, 95),
(3, 3),
(3, 10),
(3, 11),
(3, 12),
(3, 14),
(3, 17),
(3, 19),
(3, 22),
(3, 25),
(3, 28),
(3, 31),
(3, 33),
(3, 36),
(3, 38),
(3, 41),
(3, 43),
(3, 46),
(3, 48),
(3, 51),
(3, 53),
(3, 55),
(3, 57),
(3, 60),
(3, 62),
(3, 65),
(3, 68),
(3, 70),
(3, 73),
(3, 75),
(3, 78),
(3, 79),
(3, 81),
(3, 82),
(3, 83),
(3, 84),
(3, 85),
(3, 86),
(3, 88),
(3, 91),
(3, 93),
(4, 3),
(4, 10),
(4, 11),
(4, 12),
(4, 13),
(4, 14),
(4, 15),
(4, 16),
(4, 17),
(4, 18),
(4, 19),
(4, 20),
(4, 21),
(4, 22),
(4, 23),
(4, 24),
(4, 25),
(4, 26),
(4, 27),
(4, 28),
(4, 29),
(4, 30),
(4, 31),
(4, 32),
(4, 33),
(4, 34),
(4, 35),
(4, 36),
(4, 37),
(4, 38),
(4, 39),
(4, 40),
(4, 41),
(4, 42),
(4, 43),
(4, 44),
(4, 45),
(4, 46),
(4, 47),
(4, 48),
(4, 49),
(4, 50),
(4, 51),
(4, 52),
(4, 53),
(4, 54),
(4, 55),
(4, 56),
(4, 57),
(4, 58),
(4, 59),
(4, 60),
(4, 61),
(4, 62),
(4, 63),
(4, 64),
(4, 65),
(4, 66),
(4, 67),
(4, 68),
(4, 69),
(4, 70),
(4, 71),
(4, 72),
(4, 73),
(4, 74),
(4, 75),
(4, 76),
(4, 77),
(4, 78),
(4, 79),
(4, 80),
(4, 81),
(4, 82),
(4, 83),
(4, 84),
(4, 85);

-- Dump dei dati per la tabella `identity_group`
-- (Workflow system group)

INSERT INTO `identity_group` (`id`, `name`, `identity_group_identifier`) VALUES
(1, 'workflow.local', 'workflow.local');


COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
