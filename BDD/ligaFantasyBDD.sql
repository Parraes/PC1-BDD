-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         10.4.32-MariaDB - mariadb.org binary distribution
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.6.0.6765

--Creación de base de datos ligaFantasy
CREATE DATABASE IF NOT EXISTS `ligafantasyy` 
USE `ligafantasyy`;

--Creación de tabla equipo + registros e insercción de datos
CREATE TABLE IF NOT EXISTS `equipo` (
  `idEquipo` int(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `puntos` int(250) DEFAULT NULL,
  `valor` double DEFAULT NULL,
  `nJugadores` int(50) DEFAULT NULL,
  `presupuesto` double DEFAULT NULL,
  `idJugador` int(250) NOT NULL,
  `idUsuario` int(20) NOT NULL,
  `idJornada` int(11) NOT NULL,
  --llave primaria
  PRIMARY KEY (`idEquipo`),
  KEY `idUsuario` (`idUsuario`),
  KEY `idJugador` (`idJugador`),
  KEY `idJornada` (`idJornada`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--Insercción de datos
INSERT INTO `equipo` (`idEquipo`, `nombre`, `puntos`, `valor`, `nJugadores`, `presupuesto`, `idJugador`, `idUsuario`, `idJornada`) VALUES
	(7, 'Real Madrid', 62, 200000000, 26, NULL, 0, 0, 0),
	(8, 'FC Barcelona', 58, 190000000, 28, NULL, 0, 0, 0),
	(9, 'Atletico de Madrid', 49, 14000000, 25, NULL, 0, 0, 0),
	(10, 'Leganes', 54, 80000000, 19, NULL, 0, 0, 0),
	(11, 'Rayo Vallecano', 29, 90000000, 24, NULL, 0, 0, 0),
	(12, 'Villareal CF', 39, 110000000, 25, NULL, 0, 0, 0),
	(13, 'Valencia CF', 38, 130000000, 28, NULL, 0, 0, 0),
	(14, 'Girona', 59, 70000000, 21, NULL, 0, 0, 0),
	(15, 'Sevilla', 22, 120000000, 21, NULL, 0, 0, 0);

--Creación de tabla jornada + registros e insercción de datos
CREATE TABLE IF NOT EXISTS `jornada` (
  `idJornada` int(250) NOT NULL AUTO_INCREMENT,
  `nJornada` int(50) NOT NULL,
  `puntos` int(250) NOT NULL,
  `valor` double DEFAULT NULL,
  `nJugadores` int(11) DEFAULT NULL,
  `presupuesto` double DEFAULT NULL,
  `idJugador` int(11) NOT NULL,
  `idEquipo` int(11) NOT NULL,
  `puntosJugador` int(11) NOT NULL,
  --llave primaria
  PRIMARY KEY (`idJornada`),
  KEY `idEquipo` (`idEquipo`),
  KEY `idJugador` (`idJugador`),
  CONSTRAINT `FK_jornada_equipo` FOREIGN KEY (`idEquipo`) REFERENCES `equipo` (`idEquipo`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_jornada_jugador` FOREIGN KEY (`idJugador`) REFERENCES `jugador` (`idJugador`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--Insercción de datos
INSERT INTO `jornada` (`idJornada`, `nJornada`, `puntos`, `valor`, `nJugadores`, `presupuesto`, `idJugador`, `idEquipo`, `puntosJugador`) VALUES
	(3, 12, 3, NULL, NULL, NULL, 7, 7, 7),
	(5, 13, 3, NULL, NULL, NULL, 10, 9, 12),
	(6, 15, 3, 15000000, 25, NULL, 9, 8, 1),
	(7, 2, 0, 9000000, 23, 25000000, 8, 15, 5),
	(9, 3, 1, 15000000, 24, 140000000, 11, 12, 11);

--Creación de tabla jugador + registros e insercción de datos
CREATE TABLE IF NOT EXISTS `jugador` (
  `idJugador` int(11) NOT NULL AUTO_INCREMENT,
  `idEquipo` int(11) NOT NULL,
  `jugador` varchar(50) NOT NULL,
  `posicion` varchar(50) NOT NULL,
  `equipoUsuario` int(11) NOT NULL DEFAULT 0,
  `edad` int(11) DEFAULT NULL,
  `altura` double DEFAULT NULL,
  `peso` double DEFAULT NULL,
  --llave primaria
  PRIMARY KEY (`idJugador`),
  KEY `idEquipo` (`idEquipo`),
  KEY `equipoUsuario` (`equipoUsuario`),
  CONSTRAINT `FK_jugador_equipo` FOREIGN KEY (`idEquipo`) REFERENCES `equipo` (`idEquipo`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_jugador_usuario` FOREIGN KEY (`equipoUsuario`) REFERENCES `usuario` (`idUsuario`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


INSERT INTO `jugador` (`idJugador`, `idEquipo`, `jugador`, `posicion`, `equipoUsuario`, `edad`, `altura`, `peso`) VALUES
	(7, 7, 'Vinicius', 'DL', 5, 21, 1.75, 65),
	(8, 15, 'Sergio Ramos', 'DF', 7, 34, 1.83, 78.2),
	(9, 8, 'Cancelo', 'DF', 6, 29, 1, 74.2),
	(10, 9, 'Griezman', 'DL', 4, 31, 1, 69),
	(11, 13, 'Baena', 'MC', 3, 28, NULL, NULL),
  (17, 10, 'Morata', 'DL', 4, 31, 1.89, 85),
  (18, 7, 'Rodrygo', 'DL', 3, 22, 1.72, 65);

--Creación de tabla log + registros e insercción de datos
CREATE TABLE IF NOT EXISTS `log` (
  `idLog` int(11) NOT NULL AUTO_INCREMENT,
  `idUsuario` int(11) NOT NULL,
  `fechaInicio` date NOT NULL,
  `fechaFin` date DEFAULT NULL,
  PRIMARY KEY (`idLog`),
  KEY `idJugador` (`idUsuario`) USING BTREE,
  CONSTRAINT `FK_log_usuario` FOREIGN KEY (`idUsuario`) REFERENCES `usuario` (`idUsuario`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


INSERT INTO `log` (`idLog`, `idUsuario`, `fechaInicio`, `fechaFin`) VALUES
	(1, 3, '2024-06-11', '2024-07-11'),
	(3, 1, '2023-03-11', '2025-03-11'),
	(4, 6, '2024-03-19', '2024-05-11'),
	(5, 4, '2024-06-11', '2024-08-11');

--Creación de tabla notificación + registros e insercción de datos
CREATE TABLE IF NOT EXISTS `notificacion` (
  `idNotificacion` int(11) NOT NULL AUTO_INCREMENT,
  `idUsuario` int(11) NOT NULL,
  `fecha` date DEFAULT NULL,
  `descripcion` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`idNotificacion`),
  KEY `idUsuario` (`idUsuario`),
  CONSTRAINT `FK_notificacion_usuario` FOREIGN KEY (`idUsuario`) REFERENCES `usuario` (`idUsuario`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


INSERT INTO `notificacion` (`idNotificacion`, `idUsuario`, `fecha`, `descripcion`) VALUES
	(1, 1, '2024-03-12', 'Es un trampas'),
	(2, 4, '2024-03-13', 'Es un paquete, no sabe fichar...'),
	(3, 6, '2024-03-08', 'No juega por cobarde'),
	(4, 5, '2024-03-07', 'No te importa julioh'),
	(5, 7, '2024-01-11', 'Es un crack, pero tampoco es Julio Verne');

--Creación de tabla prediccionpuntos + registros e insercción de datos
CREATE TABLE IF NOT EXISTS `prediccionpuntos` (
  `idPrediccion` int(11) NOT NULL AUTO_INCREMENT,
  `idJugador` int(11) NOT NULL,
  `jornada` int(11) NOT NULL,
  `predicionPuntos` double NOT NULL,
  PRIMARY KEY (`idPrediccion`),
  KEY `idJugador` (`idJugador`),
  CONSTRAINT `FK_prediccionpuntos_jugador` FOREIGN KEY (`idJugador`) REFERENCES `jugador` (`idJugador`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


INSERT INTO `prediccionpuntos` (`idPrediccion`, `idJugador`, `jornada`, `predicionPuntos`) VALUES
	(1, 11, 12, 9),
	(2, 7, 11, 7),
	(3, 7, 1, 3),
	(4, 11, 2, 0),
	(5, 8, 5, -2),
	(6, 10, 6, 18),
	(7, 8, 3, 9);

--Creación de tabla predicionvalor + registros e insercción de datos
CREATE TABLE IF NOT EXISTS `predicionvalormercado` (
  `idPredicion` int(11) NOT NULL AUTO_INCREMENT,
  `idJugador` int(11) NOT NULL,
  `jornada` int(11) NOT NULL,
  `valorPredicion` double NOT NULL DEFAULT 0,
  PRIMARY KEY (`idPredicion`),
  KEY `idJugador` (`idJugador`),
  CONSTRAINT `FK_predicionvalormercado_jugador` FOREIGN KEY (`idJugador`) REFERENCES `jugador` (`idJugador`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


INSERT INTO `predicionvalormercado` (`idPredicion`, `idJugador`, `jornada`, `valorPredicion`) VALUES
	(1, 11, 1, 16000000),
	(2, 7, 2, 19000000),
	(3, 10, 4, 23000000),
	(4, 11, 9, 12000000),
	(5, 8, 3, 8000000),
	(6, 9, 2, 12000500),
	(7, 7, 15, 23570890),
	(8, 11, 21, 19000000);

--Creación de tabla usuario + registros e insercción de datos
CREATE TABLE IF NOT EXISTS `usuario` (
  `idUsuario` int(11) NOT NULL AUTO_INCREMENT,
  `correo` varchar(50) NOT NULL,
  `contraseña` varchar(50) NOT NULL,
  `esAdmin` tinyint(4) unsigned zerofill NOT NULL,
  `idEquipo` int(11) NOT NULL,
  PRIMARY KEY (`idUsuario`),
  KEY `idEquipo` (`idEquipo`),
  CONSTRAINT `FK_usuario_equipo` FOREIGN KEY (`idEquipo`) REFERENCES `equipo` (`idEquipo`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


INSERT INTO `usuario` (`idUsuario`, `correo`, `contraseña`, `esAdmin`, `idEquipo`) VALUES
	(1, 'manoloManolin56', 'manolito56', 0000, 7),
	(3, 'danichulo@gmail.com', 'chocoflakes123', 0000, 10),
	(4, 'guilleoas@gmail.com', 'aos2189', 0000, 9),
	(5, 'parraes@gmail.com', 'noteimporta99', 0000, 7),
	(6, 'varitovaro@hotmail.com', 'manolo00', 0000, 8),
	(7, 'juliok12@yahoo.es', 'juliito87', 0000, 15);


