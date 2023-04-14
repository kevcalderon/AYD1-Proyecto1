from conexion import obtener_conexion
from werkzeug.security import check_password_hash, generate_password_hash

# Controlador para buscar un cliente en la base de datos
def LoguearCliente(nombre_usuario, contrasenia):
    conexion = obtener_conexion()
    usuario = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT CLI_ID, CONTRASENA FROM CLIENTE c WHERE USUARIO = %s", (nombre_usuario,))
        usuario = cursor.fetchone()
        if usuario and check_password_hash(usuario[1], contrasenia):
            usuario = usuario[0]
        else:
            usuario = None
    conexion.close()
    return usuario
