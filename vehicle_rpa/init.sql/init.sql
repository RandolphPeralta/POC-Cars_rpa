CREATE DATABASE IF NOT EXISTS `vehicle_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE `vehicle_db`;

CREATE TABLE IF NOT EXISTS `autos` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `titulo` VARCHAR(255) NOT NULL,
    `precio` DECIMAL(20, 2) NULL,
    `fecha_creacion` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `error_precio` VARCHAR(255) NULL,
    UNIQUE KEY `titulo_unico` (`titulo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;