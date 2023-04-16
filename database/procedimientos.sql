DELIMITER $$
CREATE PROCEDURE CrearDireccion(
    IN MUNICIPIO_ID BIGINT,
    IN LUGAR VARCHAR(500),
    OUT DIR_ID BIGINT
)
BEGIN
    INSERT INTO DIRECCION (MUNICIPIO_MUN_ID, LUGAR) VALUES (MUNICIPIO_ID, LUGAR);
    SET DIR_ID = LAST_INSERT_ID();
END $$
DELIMITER ;