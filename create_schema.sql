CREATE DATABASE `notes2dev`;
USE `notes2dev`;
CREATE TABLE `colaborador` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `genero` varchar(1) DEFAULT NULL,
  `ativo` tinyint DEFAULT NULL,
  `gestor` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4;
CREATE TABLE `login` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `senha` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
CREATE TABLE `nota` (
  `idnota` int NOT NULL AUTO_INCREMENT,
  `data` datetime DEFAULT NULL,
  `nota` varchar(2000) DEFAULT NULL,
  `tipo` int NOT NULL,
  `colaborador` varchar(500) NOT NULL,
  PRIMARY KEY (`idnota`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4;
CREATE TABLE `tipo_nota` (
  `idtipo_nota` int NOT NULL AUTO_INCREMENT,
  `emoji` varchar(45) DEFAULT NULL,
  `tipo` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idtipo_nota`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
