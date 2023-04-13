import mysql.connector


def obtener_conexion():
    return mysql.connector.connect(host='localhost',
                                user='proyecto',
                                password='proyecto',
                                db='proyecto_db',
                                port='3307')