-- CPE422.users definition
CREATE DATABASE `CPE422` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

CREATE TABLE `users` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `note` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `image_encoding` json NOT NULL,
  `image_name` json NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_unique` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;