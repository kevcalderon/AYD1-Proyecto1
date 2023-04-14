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

# Controlador para buscar una empresa en la base de datos
def LoguearEmpresa(nombre_empresa, contrasenia):
    conexion = obtener_conexion()
    empresa = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT EMP_ID, CONTRASENA FROM EMPRESA e WHERE USUARIO = %s", (nombre_empresa,))
        empresa = cursor.fetchone()
        if empresa and check_password_hash(empresa[1], contrasenia):
            empresa = empresa[0]
        else:
            empresa = None
    conexion.close()
    return empresa
