from conexion import obtener_conexion
from werkzeug.security import check_password_hash, generate_password_hash

# Controlador para buscar un cliente en la base de datos
def LoguearCliente(nombre_usuario, contrasenia):
    conexion = obtener_conexion()
    usuario = None
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT c.CONTRASENA, c.CLI_ID, c.NOMBRE, c.APELLIDO, c.CORREO, c.TELEFONO, c.USUARIO, c.NIT, c.TARJETA, c.ESTADO, d.DIR_ID, d.LUGAR
                FROM CLIENTE c 
                INNER JOIN DIRECCION d ON d.DIR_ID = c.DIRECCION_DIR_ID 
                WHERE USUARIO = %s AND ESTADO = 'activo'
                """, (nombre_usuario,))
        usuario = cursor.fetchone()
        if usuario and check_password_hash(usuario[0], contrasenia):
            usuario = {
                # 'CONTRASENA': usuario[0],
                'CLI_ID': usuario[1],
                'NOMBRE': usuario[2],
                'APELLIDO': usuario[3],
                'CORREO': usuario[4],
                'TELEFONO': usuario[5],
                'USUARIO': usuario[6],                
                'NIT': usuario[7],
                'TARJETA': usuario[8],
                # 'ESTADO': usuario[9],
                'DIR_ID': usuario[10],
                'LUGAR': usuario[11]
            }
        else:
            usuario = None
    conexion.close()
    return usuario

# Controlador para buscar una empresa en la base de datos
def LoguearEmpresa(nombre_empresa, contrasenia):
    conexion = obtener_conexion()
    empresa = None
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT e.CONTRASENA, e.EMP_ID, e.NOMBRE AS NOMBRE_EMPRESA, e.DESCRIPCION, e.CORREO, e.TELEFONO, e.USUARIO, e.NIT, e.ESTADO, e.DOCUMENTO, 
            te.T_EMP_ID, te.NOMBRE AS NOMBRE_TIPO_EMPRESA, d.DIR_ID, d.LUGAR 
            FROM EMPRESA e
            INNER JOIN TIPO_EMPRESA te ON te.T_EMP_ID = e.TIPO_EMPRESA_T_EMP_ID 
            INNER JOIN DIRECCION d ON d.DIR_ID = e.DIRECCION_DIR_ID  WHERE USUARIO = %s AND ESTADO = 'activo'""", (nombre_empresa,))
        empresa = cursor.fetchone()
        if empresa and check_password_hash(empresa[0], contrasenia):
            empresa = {
                # 'CONTRASENA': empresa[0],
                'EMP_ID': empresa[1],
                'NOMBRE_EMPRESA': empresa[2],
                'DESCRIPCION': empresa[3],
                'CORREO': empresa[4],
                'TELEFONO': empresa[5],
                'USUARIO': empresa[6],                
                'NIT': empresa[7],
                # 'ESTADO': empresa[8],
                'DOCUMENTO': empresa[9],
                'T_EMP_ID': empresa[10],
                'NOMBRE_TIPO_EMPRESA': empresa[11],
                'DIR_ID': empresa[12],
                'LUGAR': empresa[13],
            }
        else:
            empresa = None
    conexion.close()
    return empresa

# Controlador para ver todos los departamentos en la base de datos
def VerDepartamentos():
    conexion = obtener_conexion()
    departamentos = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM DEPARTAMENTO d")
        departamentos = cursor.fetchall()
        departamentos = [{"DEP_ID":departamento[0], "NOMBRE":departamento[1]}for departamento in departamentos]
    conexion.close()
    return departamentos

# Controlador para ver todos los municipios en la base de datos
def VerMunicipios():
    conexion = obtener_conexion()
    municipios = []
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT m.MUN_ID, m.NOMBRE AS NOMBRE_MUNICIPIO, d.DEP_ID, d.NOMBRE AS NOMBRE_DEPARTAMENTO
        FROM MUNICIPIO m 
        INNER JOIN DEPARTAMENTO d ON d.DEP_ID = m.DEPARTAMENTO_DEP_ID""")
        municipios = cursor.fetchall()
        municipios = [{"MUN_ID":municipio[0], "NOMBRE_MUNICIPIO":municipio[1], "DEP_ID":municipio[2], "NOMBRE_DEPARTAMENTO":municipio[3]}for municipio in municipios]
    conexion.close()
    return municipios
