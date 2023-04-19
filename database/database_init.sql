CREATE TABLE ADMINISTRADOR
(
USUARIO VARCHAR(25) NOT NULL ,
CONTRASENA VARCHAR(25) NOT NULL
);

CREATE TABLE DIRECCION
(
DIR_ID BIGINT NOT NULL AUTO_INCREMENT,
MUNICIPIO_MUN_ID BIGINT NOT NULL ,
LUGAR VARCHAR(500) NOT NULL ,
PRIMARY KEY (DIR_ID)
);

CREATE TABLE CLIENTE
(
CLI_ID BIGINT NOT NULL AUTO_INCREMENT,
DIRECCION_DIR_ID BIGINT NOT NULL ,
NOMBRE VARCHAR(250) NOT NULL ,
APELLIDO VARCHAR(250) NOT NULL ,
CORREO VARCHAR(300) NOT NULL ,
TELEFONO VARCHAR(15) NOT NULL ,
USUARIO VARCHAR(250) NOT NULL ,
CONTRASENA VARCHAR(250) NOT NULL ,
NIT VARCHAR(15) ,
TARJETA VARCHAR(20) NOT NULL ,
ESTADO VARCHAR(50) NOT NULL ,
PRIMARY KEY (CLI_ID)
);

CREATE TABLE TIPO_EMPRESA (
T_EMP_ID BIGINT NOT NULL AUTO_INCREMENT,
NOMBRE VARCHAR(250) NOT NULL,
PRIMARY KEY (T_EMP_ID)
);

CREATE TABLE EMPRESA
(
EMP_ID BIGINT NOT NULL AUTO_INCREMENT,
DIRECCION_DIR_ID BIGINT NOT NULL ,
TIPO_EMPRESA_T_EMP_ID BIGINT NOT NULL ,
NOMBRE VARCHAR(250) NOT NULL ,
DESCRIPCION VARCHAR(500) NOT NULL ,
CORREO VARCHAR(300) NOT NULL ,
TELEFONO VARCHAR(15) NOT NULL ,
USUARIO VARCHAR(250) NOT NULL ,
CONTRASENA VARCHAR(250) NOT NULL ,
NIT VARCHAR(15) NOT NULL ,
ESTADO VARCHAR(20) NOT NULL ,
DOCUMENTO TEXT ,
PRIMARY KEY (EMP_ID)
);


CREATE TABLE REPARTIDOR (
REP_ID BIGINT NOT NULL AUTO_INCREMENT,
DIRECCION_DIR_ID BIGINT NOT NULL,
NOMBRE VARCHAR(250) NOT NULL,
APELLIDO VARCHAR(250) NOT NULL,
CORREO VARCHAR(300) NOT NULL,
TELEFONO VARCHAR(15) NOT NULL,
USUARIO VARCHAR(250) NOT NULL,
CONTRASENA VARCHAR(250) NOT NULL,
NIT VARCHAR(15) NOT NULL,
ESTADO VARCHAR(20) NOT NULL,
DOCUMENTO TEXT,
LICENCIA VARCHAR(10) NOT NULL,
TRANSPORTE VARCHAR(10) NOT NULL,
PRIMARY KEY (REP_ID)
);

CREATE TABLE TIPO_PRODUCTO (
T_PRO_ID BIGINT NOT NULL AUTO_INCREMENT,
NOMBRE VARCHAR(250) NOT NULL,
PRIMARY KEY (T_PRO_ID)
);

CREATE TABLE PRODUCTO (
PRO_ID BIGINT NOT NULL AUTO_INCREMENT,
EMPRESA_EMP_ID BIGINT NOT NULL,
TIPO_PRODUCTO_T_PRO_ID BIGINT NOT NULL,
NOMBRE VARCHAR(250) NOT NULL,
DESCRIPCION VARCHAR(500) NOT NULL,
PRECIO BIGINT NOT NULL,
STOCK BIGINT NOT NULL,
FOTOGRAFIA TEXT NOT NULL,
PRIMARY KEY (PRO_ID)
);

CREATE TABLE ORDEN (
ORD_ID BIGINT NOT NULL AUTO_INCREMENT,
CLIENTE_CLI_ID BIGINT NOT NULL,
DIRECCION_DIR_ID BIGINT NOT NULL,
REPARTIDOR_REP_ID BIGINT,
FECHA DATETIME NOT NULL,
ESTADO VARCHAR(20) NOT NULL,
CALIFICACION BIGINT,
COMENTARIO VARCHAR(500),
METODO_PAGO VARCHAR(100) NOT NULL,
PRIMARY KEY (ORD_ID)
);


CREATE TABLE COMBO
(
COM_ID BIGINT NOT NULL AUTO_INCREMENT,
NOMBRE VARCHAR(250) NOT NULL ,
DESCRIPCION VARCHAR(500) NOT NULL ,
PRECIO BIGINT NOT NULL ,
FOTOGRAFIA TEXT NOT NULL,
PRIMARY KEY (COM_ID)
);

CREATE TABLE DEPARTAMENTO
(
DEP_ID BIGINT NOT NULL AUTO_INCREMENT,
NOMBRE VARCHAR(250) NOT NULL ,
PRIMARY KEY (DEP_ID)
);

CREATE TABLE DETALLE_COMBO
(
COMBO_COM_ID BIGINT NOT NULL ,
PRODUCTO_PRO_ID BIGINT NOT NULL ,
CANTIDAD BIGINT NOT NULL ,
OBSERVACIONES VARCHAR(500)
);

CREATE TABLE DETALLE_ORDEN
(
COMBO_COM_ID BIGINT ,
ORDEN_ORD_ID BIGINT NOT NULL ,
PRODUCTO_PRO_ID BIGINT ,
CANTIDAD BIGINT NOT NULL ,
OBSERVACIONES VARCHAR(500) ,
ESTADO VARCHAR(20) NOT NULL
);

CREATE TABLE INHABILITACION (
EMPRESA_EMP_ID BIGINT,
REPARTIDOR_REP_ID BIGINT,
CLIENTE_CLI_ID BIGINT,
TIPO_INHABILITACION VARCHAR(100) NOT NULL,
FECHA DATETIME NOT NULL,
DESCRIPCION VARCHAR(500) NOT NULL,
ESTADO VARCHAR(20) NOT NULL
);

CREATE TABLE MUNICIPIO (
MUN_ID BIGINT NOT NULL AUTO_INCREMENT,
DEPARTAMENTO_DEP_ID BIGINT NOT NULL,
NOMBRE VARCHAR(250) NOT NULL,
PRIMARY KEY (MUN_ID)
);


CREATE TABLE SOLICITUD (
EMPRESA_EMP_ID BIGINT,
REPARTIDOR_REP_ID BIGINT,
TIPO_SOLICITUD VARCHAR(100) NOT NULL,
FECHA DATETIME NOT NULL,
DESCRIPCION VARCHAR(500) NOT NULL,
ESTADO VARCHAR(20) NOT NULL
);


CREATE TABLE VENTA (
ORDEN_ORD_ID BIGINT NOT NULL,
FECHA DATETIME NOT NULL,
TOTAL BIGINT NOT NULL
);

ALTER TABLE CLIENTE ADD CONSTRAINT CLIENTE_DIRECCION_FK FOREIGN KEY (DIRECCION_DIR_ID) REFERENCES DIRECCION(DIR_ID) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE DETALLE_COMBO ADD CONSTRAINT DETALLE_COMBO_COMBO_FK FOREIGN KEY (COMBO_COM_ID) REFERENCES COMBO(COM_ID) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE DETALLE_COMBO ADD CONSTRAINT DETALLE_COMBO_PRODUCTO_FK FOREIGN KEY (PRODUCTO_PRO_ID) REFERENCES PRODUCTO(PRO_ID) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE DETALLE_ORDEN ADD CONSTRAINT DETALLE_ORDEN_COMBO_FK FOREIGN KEY (COMBO_COM_ID) REFERENCES COMBO(COM_ID) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE DETALLE_ORDEN ADD CONSTRAINT DETALLE_ORDEN_ORDEN_FK FOREIGN KEY (ORDEN_ORD_ID) REFERENCES ORDEN(ORD_ID) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE DETALLE_ORDEN ADD CONSTRAINT DETALLE_ORDEN_PRODUCTO_FK FOREIGN KEY (PRODUCTO_PRO_ID) REFERENCES PRODUCTO(PRO_ID) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE DIRECCION ADD CONSTRAINT DIRECCION_MUNICIPIO_FK FOREIGN KEY (MUNICIPIO_MUN_ID) REFERENCES MUNICIPIO(MUN_ID) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE EMPRESA ADD CONSTRAINT EMPRESA_DIRECCION_FK FOREIGN KEY (DIRECCION_DIR_ID) REFERENCES DIRECCION(DIR_ID) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE EMPRESA ADD CONSTRAINT EMPRESA_TIPO_EMPRESA_FK FOREIGN KEY (TIPO_EMPRESA_T_EMP_ID) REFERENCES TIPO_EMPRESA(T_EMP_ID) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE INHABILITACION ADD CONSTRAINT INHABILITACION_CLIENTE_FK FOREIGN KEY (CLIENTE_CLI_ID) REFERENCES CLIENTE(CLI_ID) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE INHABILITACION ADD CONSTRAINT INHABILITACION_EMPRESA_FK FOREIGN KEY (EMPRESA_EMP_ID) REFERENCES EMPRESA(EMP_ID) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE INHABILITACION ADD CONSTRAINT INHABILITACION_REPARTIDOR_FK FOREIGN KEY (REPARTIDOR_REP_ID) REFERENCES REPARTIDOR(REP_ID) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE MUNICIPIO ADD CONSTRAINT MUNICIPIO_DEPARTAMENTO_FK FOREIGN KEY (DEPARTAMENTO_DEP_ID) REFERENCES DEPARTAMENTO(DEP_ID) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE ORDEN ADD CONSTRAINT ORDEN_CLIENTE_FK FOREIGN KEY (CLIENTE_CLI_ID) REFERENCES CLIENTE (CLI_ID) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE ORDEN ADD CONSTRAINT ORDEN_DIRECCION_FK FOREIGN KEY (DIRECCION_DIR_ID) REFERENCES DIRECCION (DIR_ID) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE ORDEN ADD CONSTRAINT ORDEN_REPARTIDOR_FK FOREIGN KEY (REPARTIDOR_REP_ID) REFERENCES REPARTIDOR (REP_ID) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE PRODUCTO ADD CONSTRAINT PRODUCTO_EMPRESA_FK FOREIGN KEY (EMPRESA_EMP_ID) REFERENCES EMPRESA (EMP_ID) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE PRODUCTO ADD CONSTRAINT PRODUCTO_TIPO_PRODUCTO_FK FOREIGN KEY (TIPO_PRODUCTO_T_PRO_ID) REFERENCES TIPO_PRODUCTO(T_PRO_ID) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE REPARTIDOR ADD CONSTRAINT REPARTIDOR_DIRECCION_FK FOREIGN KEY (DIRECCION_DIR_ID) REFERENCES DIRECCION (DIR_ID) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE SOLICITUD ADD CONSTRAINT SOLICITUD_EMPRESA_FK FOREIGN KEY (EMPRESA_EMP_ID) REFERENCES EMPRESA (EMP_ID) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE SOLICITUD ADD CONSTRAINT SOLICITUD_REPARTIDOR_FK FOREIGN KEY (REPARTIDOR_REP_ID) REFERENCES REPARTIDOR(REP_ID) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE VENTA ADD CONSTRAINT VENTA_ORDEN_FK FOREIGN KEY (ORDEN_ORD_ID) REFERENCES ORDEN(ORD_ID) ON DELETE NO ACTION ON UPDATE NO ACTION;



INSERT INTO DEPARTAMENTO (nombre) VALUES ('Alta Verapaz');
INSERT INTO DEPARTAMENTO (nombre) VALUES ('Baja Verapaz');
INSERT INTO DEPARTAMENTO (nombre) VALUES ('Chimaltenango');
INSERT INTO DEPARTAMENTO (nombre) VALUES ('Chiquimula');
INSERT INTO DEPARTAMENTO (nombre) VALUES ('El Progreso');
INSERT INTO DEPARTAMENTO (nombre) VALUES ('Escuintla');
INSERT INTO DEPARTAMENTO (nombre) VALUES ('Guatemala');
INSERT INTO DEPARTAMENTO (nombre) VALUES ('Huehuetenango');
INSERT INTO DEPARTAMENTO (nombre) VALUES ('Izabal');
INSERT INTO DEPARTAMENTO (nombre) VALUES ('Jalapa');
INSERT INTO DEPARTAMENTO (nombre) VALUES ('Jutiapa');
INSERT INTO DEPARTAMENTO (nombre) VALUES ('Petén');
INSERT INTO DEPARTAMENTO (nombre) VALUES ('Quetzaltenango');
INSERT INTO DEPARTAMENTO (nombre) VALUES ('Quiché');
INSERT INTO DEPARTAMENTO (nombre) VALUES ('Retalhuleu');
INSERT INTO DEPARTAMENTO (nombre) VALUES ('Sacatepéquez');
INSERT INTO DEPARTAMENTO (nombre) VALUES ('San Marcos');
INSERT INTO DEPARTAMENTO (nombre) VALUES ('Santa Rosa');
INSERT INTO DEPARTAMENTO (nombre) VALUES ('Sololá');
INSERT INTO DEPARTAMENTO (nombre) VALUES ('Suchitepéquez');
INSERT INTO DEPARTAMENTO (nombre) VALUES ('Totonicapán');
INSERT INTO DEPARTAMENTO (nombre) VALUES ('Zacapa');

-- INSERTAR MUNICIPIOS

-- Municipios de Alta Verapaz
INSERT INTO MUNICIPIO (nombre, DEPARTAMENTO_DEP_ID) VALUES
('Cobán', 1),
('Chahal', 1),
('Fray Bartolomé de las Casas', 1),
('Lanquín', 1),
('Panzós', 1),
('San Cristóbal Verapaz', 1),
('San Juan Chamelco', 1),
('San Pedro Carchá', 1),
('Santa Cruz Verapaz', 1),
('Santa María Cahabón', 1),
('Senahú', 1),
('Tactic', 1),
('Tamahú', 1),
('Tucurú', 1);

-- Municipios de Baja Verapaz
INSERT INTO MUNICIPIO (nombre, DEPARTAMENTO_DEP_ID) VALUES
('Cubulco', 2),
('Granados', 2),
('Purulhá', 2),
('Rabinal', 2),
('Salamá', 2),
('San Jerónimo', 2),
('San Miguel Chicaj', 2),
('Santa Cruz El Chol', 2);

-- Municipios de Chimaltenango
INSERT INTO MUNICIPIO(nombre, DEPARTAMENTO_DEP_ID) VALUES
('Chimaltenango', 3),
('San José Poaquil', 3),
('San Martín Jilotepeque', 3),
('San Juan Comalapa', 3),
('Santa Apolonia', 3),
('Tecpán Guatemala', 3),
('Patzicía', 3),
('Patzún', 3),
('Pochuta', 3),
('San Miguel Pochuta', 3),
('Santa Cruz Balanyá', 3),
('Acatenango', 3),
('San Pedro Yepocapa', 3),
('San Andrés Itzapa', 3),
('Parramos', 3),
('Zaragoza', 3);

-- Municipios de Chiquimula
INSERT INTO MUNICIPIO (nombre, DEPARTAMENTO_DEP_ID) VALUES
('Chiquimula', 4),
('San José La Arada', 4),
('San Juan Ermita', 4),
('Jocotán', 4),
('Camotán', 4),
('Olopa', 4),
('Esquipulas', 4),
('Quezaltepeque', 4),
('San Jacinto', 4),
('Ipala', 4);

-- Municipios de El Progreso
INSERT INTO MUNICIPIO (nombre, DEPARTAMENTO_DEP_ID) VALUES
('Guastatoya', 5),
('El Jícaro', 5),
('Sanarate', 5),
('Sansare', 5),
('San Agustín Acasaguastlán', 5),
('San Antonio La Paz', 5),
('San Cristóbal Acasaguastlán', 5),
('Cachí', 5),
('Morazán', 5),
('El Rancho', 5),
('Las Pilas', 5),
('El Progreso', 5);

-- Municipios de Escuintla
INSERT INTO MUNICIPIO (nombre, DEPARTAMENTO_DEP_ID) VALUES
('Escuintla', 6),
('Santa Lucía Cotzumalguapa', 6),
('La Democracia', 6),
('Siquinalá', 6),
('Masagua', 6),
('Tiquisate', 6),
('La Gomera', 6),
('Guanagazapa', 6),
('San José', 6),
('Iztapa', 6);


-- Municipios de Guatemala
INSERT INTO MUNICIPIO (nombre, DEPARTAMENTO_DEP_ID) VALUES
('Guatemala', 7),
('Amatitlán', 7),
('Chinautla', 7),
('Chuarrancho', 7),
('Fraijanes', 7),
('Mixco', 7),
('Palencia', 7),
('San Miguel Petapa', 7),
('San José del Golfo', 7),
('San José Pinula', 7),
('San Juan Sacatepéquez', 7),
('San Pedro Ayampuc', 7),
('San Pedro Sacatepéquez', 7),
('San Raymundo', 7),
('Santa Catarina Pinula', 7),
('Villa Canales', 7),
('Villa Nueva', 7);


-- Municipios de Huehuetenango
INSERT INTO MUNICIPIO (nombre, DEPARTAMENTO_DEP_ID) VALUES
('Aguacatán', 8),
('Chiantla', 8),
('Colotenango', 8),
('Concepción Huista', 8),
('Cuilco', 8),
('Huehuetenango', 8),
('Jacaltenango', 8),
('La Democracia', 8),
('La Libertad', 8),
('Malacatancito', 8),
('Nentón', 8),
('Petatán', 8),
('San Antonio Huista', 8),
('San Gaspar Ixchil', 8),
('San Ildefonso Ixtahuacán', 8),
('San Juan Atitán', 8),
('San Juan Ixcoy', 8),
('San Mateo Ixtatán', 8),
('San Miguel Acatán', 8),
('San Pedro Necta', 8),
('San Pedro Soloma', 8),
('San Rafael La Independencia', 8),
('San Rafael Petzal', 8),
('San Sebastián Coatán', 8),
('San Sebastián Huehuetenango', 8),
('Santa Ana Huista', 8),
('Santa Bárbara', 8),
('Santa Cruz Barillas', 8),
('Santa Eulalia', 8),
('Santiago Chimaltenango', 8),
('Soloma', 8),
('Tectitán', 8);

-- Municipios de Izabal
INSERT INTO MUNICIPIO (nombre, DEPARTAMENTO_DEP_ID) VALUES
('Puerto Barrios', 9),
('Livingston', 9),
('El Estor', 9),
('Morales', 9),
('Los Amates', 9);

-- Insertar municipios de Jalapa
INSERT INTO MUNICIPIO (nombre, DEPARTAMENTO_DEP_ID) VALUES
('Jalapa', 10),
('San Pedro Pinula', 10),
('San Luis Jilotepeque', 10),
('San Manuel Chaparrón', 10),
('San Carlos Alzatate', 10),
('Monjas', 10),
('Mataquescuintla', 10);

-- Municipios de Jutiapa
INSERT INTO MUNICIPIO (nombre, DEPARTAMENTO_DEP_ID) VALUES
('Jutiapa', 11),
('El Progreso', 11),
('Agua Blanca', 11),
('Asunción Mita', 11),
('Atescatempa', 11),
('Comapa', 11),
('Conguaco', 11),
('El Adelanto', 11),
('El Progreso', 11),
('Jalpatagua', 11),
('Jerez', 11),
('Moyuta', 11),
('Pasaco', 11),
('Quezada', 11),
('San José Acatempa', 11),
('Santa Catarina Mita', 11),
('Yupiltepeque', 11);

-- Municipios de Petén
INSERT INTO MUNICIPIO (nombre, DEPARTAMENTO_DEP_ID) VALUES
('Dolores', 12),
('Flores', 12),
('La Libertad', 12),
('Las Cruces', 12),
('Melchor de Mencos', 12),
('Poptún', 12),
('San Andrés', 12),
('San Benito', 12),
('San Francisco', 12),
('San José', 12),
('San Luis', 12),
('Santa Ana', 12),
('Sayaxché', 12);

-- Municipios de Quetzaltenango
INSERT INTO MUNICIPIO (nombre, DEPARTAMENTO_DEP_ID) VALUES
('Almolonga', 13),
('Cabricán', 13),
('Cajolá', 13),
('Cantel', 13),
('Coatepeque', 13),
('Colomba', 13),
('Concepción Chiquirichapa', 13),
('El Palmar', 13),
('Flores Costa Cuca', 13),
('Génova', 13),
('Huitán', 13),
('La Esperanza', 13),
('Olintepeque', 13),
('Ostuncalco', 13),
('Palestina de los Altos', 13),
('Quetzaltenango', 13),
('Salcajá', 13),
('San Carlos Sija', 13),
('San Francisco La Unión', 13),
('San Juan Ostuncalco', 13),
('San Martín Sacatepéquez', 13),
('San Mateo', 13),
('San Miguel Sigüilá', 13),
('Sibilia', 13),
('Zunil', 13);

-- Municipios de Quiché
INSERT INTO MUNICIPIO (nombre, DEPARTAMENTO_DEP_ID) VALUES
('Santa Cruz del Quiché', 14),
('Canillá', 14),
('Chajul', 14),
('Chicamán', 14),
('Chiché', 14),
('Chinique', 14),
('Cunén', 14),
('Joyabaj', 14),
('Nebaj', 14),
('Pachalum', 14),
('Patzité', 14),
('Sacapulas', 14),
('San Andrés Sajcabajá', 14),
('San Antonio Ilotenango', 14),
('San Bartolomé Jocotenango', 14),
('San Juan Cotzal', 14),
('San Pedro Jocopilas', 14),
('Uspantán', 14);

-- Municipios de Retalhuleu
INSERT INTO MUNICIPIO (nombre, DEPARTAMENTO_DEP_ID) VALUES
('Retalhuleu', 15),
('San Sebastián', 15),
('Santa Cruz Muluá', 15),
('San Martín Zapotitlán', 15),
('San Felipe', 15),
('San Andrés Villa Seca', 15), 
('Champerico', 15),
('Nuevo San Carlos', 15);


-- Municipios de Sacatepéquez
INSERT INTO MUNICIPIO (nombre, DEPARTAMENTO_DEP_ID) VALUES
('Antigua Guatemala', 16),
('Ciudad Vieja', 16),
('Jocotenango', 16),
('Magdalena Milpas Altas', 16),
('Pastores', 16),
('San Antonio Aguas Calientes', 16),
('San Bartolomé Milpas Altas', 16),
('San Lucas Sacatepéquez', 16),
('San Miguel Dueñas', 16),
('Santa Catarina Barahona', 16),
('Santa Lucía Milpas Altas', 16),
('Santiago Sacatepéquez', 16),
('Santo Domingo Xenacoj', 16);

-- Municipios de San Marcos
INSERT INTO MUNICIPIO (nombre, DEPARTAMENTO_DEP_ID) VALUES
('San Marcos', 17),
('Ayutla', 17),
('Catarina', 17),
('Comitancillo', 17),
('Concepción Tutuapa', 17),
('El Quetzal', 17),
('El Rodeo', 17),
('El Tumbador', 17),
('Esquipulas Palo Gordo', 17),
('Ixchiguán', 17),
('La Reforma', 17),
('Malacatán', 17),
('Nuevo Progreso', 17),
('Ocos', 17),
('Pajapita', 17),
('Río Blanco', 17),
('San Cristóbal Cucho', 17),
('San José Ojetenam', 17),
('San Lorenzo', 17),
('San Miguel Ixtahuacán', 17),
('San Pablo', 17),
('San Rafael Pie de la Cuesta', 17),
('Sibinal', 17),
('Sipacapa', 17),
('Tacaná', 17),
('Tajumulco', 17),
('Tejutla', 17);


-- Municipios de Santa Rosa
INSERT INTO MUNICIPIO (nombre, DEPARTAMENTO_DEP_ID) VALUES
('Cuilapa', 18),
('Barberena', 18),
('Casillas', 18),
('Chiquimulilla', 18),
('Guazacapán', 18),
('Nueva Santa Rosa', 18),
('Oratorio', 18),
('Pueblo Nuevo Viñas', 18),
('San Juan Tecuaco', 18),
('San Rafael Las Flores', 18),
('Santa Cruz Naranjo', 18),
('Santa María Ixhuatán', 18),
('Santa Rosa de Lima', 18),
('Taxisco', 18);


-- Municipios de Sololá
INSERT INTO MUNICIPIO (nombre, DEPARTAMENTO_DEP_ID) VALUES
('Sololá', 19),
('San José Chacayá', 19),
('Santa María Visitación', 19),
('Santa Lucía Utatlán', 19),
('Nahualá', 19),
('Santa Catarina Ixtahuacán', 19),
('Santa Clara La Laguna', 19),
('Concepción', 19),
('San Andrés Semetabaj', 19),
('Panajachel', 19),
('Santa Catarina Palopó', 19),
('San Antonio Palopó', 19),
('San Lucas Tolimán', 19),
('Santa Cruz La Laguna', 19),
('San Pablo La Laguna', 19),
('San Juan La Laguna', 19),
('San Marcos La Laguna', 19),
('Santa Bárbara', 19),
('San Pedro La Laguna', 19),
('Santiago Atitlán', 19);


-- Municipios de Suchitepequez
INSERT INTO MUNICIPIO (nombre, DEPARTAMENTO_DEP_ID) VALUES
('Mazatenango', 20),
('Cuyotenango', 20),
('San Francisco Zapotitlán', 20),
('San Bernardino', 20),
('San José El Ídolo', 20),
('Santo Domingo Suchitepéquez', 20),
('San Lorenzo', 20),
('Samayac', 20),
('San Pablo Jocopilas', 20),
('San Antonio Suchitepéquez', 20),
('Patulul', 20),
('Chicacao', 20),
('Pueblo Nuevo', 20);


-- Municipios de Totonicapán
INSERT INTO MUNICIPIO (nombre, DEPARTAMENTO_DEP_ID) VALUES
('Momostenango', 21),
('Totonicapán', 21),
('San Cristóbal Totonicapán', 21),
('San Francisco El Alto', 21),
('Santa Lucía La Reforma', 21),
('San Andrés Xecul', 21),
('San Bartolo', 21),
('San Antonio Sija', 21),
('San Francisco Oxlajuj Noj', 21);


-- Municipios de Zacapa
INSERT INTO MUNICIPIO (nombre, DEPARTAMENTO_DEP_ID) VALUES
('Zacapa', 22),
('Cabañas', 22),
('Estanzuela', 22),
('Gualán', 22),
('Huité', 22),
('La Unión', 22),
('Río Hondo', 22),
('San Diego', 22),
('Teculután', 22),
('Usumatlán', 22);

-- INSERTAR LAS CATEGORIAS DE LAS EMPRESAS
INSERT INTO TIPO_EMPRESA (nombre) VALUES
('RESTAURANTES'),
('TIENDAS DE CONVENIENCIA'),
('SUPERMERCADOS');

-- INSERTAR LAS CATEGORIAS DE LOS PRODUCTOS
INSERT INTO TIPO_PRODUCTO (nombre) VALUES
('ENTRADAS'),
('PLATOS FUERTES'),
('POSTRES'),
('BEBIDAS'),
('PRODUCTOS DE ASEO'),
('LIBRERIA'),
('FERRETERIA'),
('SNACKS'),
('ELECTRONICOS'),
('ARTICULOS DEPORTIVOS'),
('VESTUARIO');

-- INSERTAR USUARIO ADMINISTRADOR
INSERT INTO ADMINISTRADOR (USUARIO, CONTRASENA) VALUES ('admin', 'admin');