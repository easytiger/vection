BEGIN;
CREATE TABLE `core_projectcomponent` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(50) NOT NULL,
    `desc` varchar(100) NOT NULL,
    `default_engineer_id` integer NOT NULL,
    `project_for_component_id` integer NOT NULL
);
CREATE TABLE `core_project` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(30) NOT NULL,
    `tag` varchar(5) NOT NULL UNIQUE,
    `desc` longtext NOT NULL,
    `project_lead_id` integer NOT NULL
);
ALTER TABLE `core_projectcomponent` ADD CONSTRAINT project_for_component_id_refs_id_42104aa2 FOREIGN KEY (`project_for_component_id`) REFERENCES `core_project` (`id`);
CREATE TABLE `core_issueupdate` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `fields` longtext NULL,
    `comment` longtext NOT NULL,
    `made` datetime NOT NULL,
    `user_id` integer NOT NULL,
    `issue_id` integer NULL
);
CREATE TABLE `core_issue` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `title` varchar(100) NOT NULL,
    `issue_type_id` integer NOT NULL,
    `project_id` integer NOT NULL REFERENCES `core_project` (`id`),
    `sub_component_id` integer NOT NULL REFERENCES `core_projectcomponent` (`id`),
    `priority_id` integer NOT NULL,
    `status_id` integer NULL,
    `resolution_id` integer NULL,
    `description` longtext NOT NULL,
    `version_id` integer NULL,
    `environment` longtext NULL,
    `created_by_id` integer NOT NULL,
    `responsible_user_id` integer NOT NULL,
    `due_date` date NULL,
    `created` datetime NOT NULL,
    `last_updated` datetime NOT NULL
);
ALTER TABLE `core_issueupdate` ADD CONSTRAINT issue_id_refs_id_5b8e406d FOREIGN KEY (`issue_id`) REFERENCES `core_issue` (`id`);
CREATE TABLE `core_priority` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(10) NOT NULL,
    `description` varchar(60) NOT NULL,
    `icon` varchar(250) NOT NULL,
    `position` integer UNSIGNED NOT NULL,
    `colour` varchar(10) NOT NULL
);
ALTER TABLE `core_issue` ADD CONSTRAINT priority_id_refs_id_45785c9a FOREIGN KEY (`priority_id`) REFERENCES `core_priority` (`id`);
CREATE TABLE `core_projectversion` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(30) NOT NULL,
    `released` bool NULL,
    `release_date` date NULL,
    `unnasigned` bool NOT NULL,
    `project_for_version_id` integer NOT NULL REFERENCES `core_project` (`id`)
);
ALTER TABLE `core_issue` ADD CONSTRAINT version_id_refs_id_7d6a633d FOREIGN KEY (`version_id`) REFERENCES `core_projectversion` (`id`);
CREATE TABLE `core_status` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `status` varchar(20) NOT NULL,
    `description` varchar(100) NOT NULL,
    `position` integer UNSIGNED NOT NULL,
    `icon` varchar(250) NULL
);
ALTER TABLE `core_issue` ADD CONSTRAINT status_id_refs_id_728dea02 FOREIGN KEY (`status_id`) REFERENCES `core_status` (`id`);
CREATE TABLE `core_issuetype` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `type` varchar(20) NOT NULL,
    `description` varchar(100) NOT NULL,
    `icon` varchar(120) NULL,
    `position` integer UNSIGNED NOT NULL
);
ALTER TABLE `core_issue` ADD CONSTRAINT issue_type_id_refs_id_3fc76dac FOREIGN KEY (`issue_type_id`) REFERENCES `core_issuetype` (`id`);
CREATE TABLE `core_resolution` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `type` varchar(20) NOT NULL,
    `description` varchar(100) NOT NULL
);
ALTER TABLE `core_issue` ADD CONSTRAINT resolution_id_refs_id_81efb36 FOREIGN KEY (`resolution_id`) REFERENCES `core_resolution` (`id`);
CREATE TABLE `core_userprofile` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `url` varchar(200) NOT NULL,
    `user_id` integer NOT NULL UNIQUE REFERENCES `auth_user` (`id`),
    `avatar_url` varchar(200) NULL,
    `tagline` varchar(50) NOT NULL
);
ALTER TABLE `core_projectcomponent` ADD CONSTRAINT default_engineer_id_refs_id_58ce2ba1 FOREIGN KEY (`default_engineer_id`) REFERENCES `core_userprofile` (`id`);
ALTER TABLE `core_project` ADD CONSTRAINT project_lead_id_refs_id_1f91861f FOREIGN KEY (`project_lead_id`) REFERENCES `core_userprofile` (`id`);
ALTER TABLE `core_issueupdate` ADD CONSTRAINT user_id_refs_id_128f8324 FOREIGN KEY (`user_id`) REFERENCES `core_userprofile` (`id`);
ALTER TABLE `core_issue` ADD CONSTRAINT created_by_id_refs_id_4e3779b7 FOREIGN KEY (`created_by_id`) REFERENCES `core_userprofile` (`id`);
ALTER TABLE `core_issue` ADD CONSTRAINT responsible_user_id_refs_id_4e3779b7 FOREIGN KEY (`responsible_user_id`) REFERENCES `core_userprofile` (`id`);
CREATE INDEX core_projectcomponent_default_engineer_id ON `core_projectcomponent` (`default_engineer_id`);
CREATE INDEX core_projectcomponent_project_for_component_id ON `core_projectcomponent` (`project_for_component_id`);
CREATE INDEX core_project_project_lead_id ON `core_project` (`project_lead_id`);
CREATE INDEX core_issueupdate_user_id ON `core_issueupdate` (`user_id`);
CREATE INDEX core_issueupdate_issue_id ON `core_issueupdate` (`issue_id`);
CREATE INDEX core_issue_issue_type_id ON `core_issue` (`issue_type_id`);
CREATE INDEX core_issue_project_id ON `core_issue` (`project_id`);
CREATE INDEX core_issue_sub_component_id ON `core_issue` (`sub_component_id`);
CREATE INDEX core_issue_priority_id ON `core_issue` (`priority_id`);
CREATE INDEX core_issue_status_id ON `core_issue` (`status_id`);
CREATE INDEX core_issue_resolution_id ON `core_issue` (`resolution_id`);
CREATE INDEX core_issue_version_id ON `core_issue` (`version_id`);
CREATE INDEX core_issue_created_by_id ON `core_issue` (`created_by_id`);
CREATE INDEX core_issue_responsible_user_id ON `core_issue` (`responsible_user_id`);
CREATE INDEX core_projectversion_project_for_version_id ON `core_projectversion` (`project_for_version_id`);
CREATE UNIQUE INDEX core_userprofile_user_id ON `core_userprofile` (`user_id`);
COMMIT;
