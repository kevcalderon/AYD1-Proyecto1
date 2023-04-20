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

# Controlador para ver todos los tipos de empresa en la base de datos
def VerTiposEmpresa():
    conexion = obtener_conexion()
    tipos_empresa = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM TIPO_EMPRESA te")
        tipos_empresa = cursor.fetchall()
        tipos_empresa = [{"T_EMP_ID":tipo_empresa[0], "NOMBRE":tipo_empresa[1]}for tipo_empresa in tipos_empresa]
    conexion.close()
    return tipos_empresa

# Controlador para buscar una direccion existente en la base de datos
def ObtenerDireccion(id_municipio, lugar):
    conexion = obtener_conexion()
    direccion = None
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT DIR_ID FROM DIRECCION d WHERE MUNICIPIO_MUN_ID = %s AND UPPER(LUGAR) = UPPER(%s)""", (id_municipio, lugar,))
        direccion = cursor.fetchone()
    conexion.close()
    return direccion

# Controlador para buscar un usuario de tipo empresa existente en la base de datos.
def ObtenerUsuarioEmpresa(nombre_usuario):
    conexion = obtener_conexion()
    usuario = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT EMP_ID FROM EMPRESA e WHERE UPPER(USUARIO) = UPPER(%s)", (nombre_usuario,))
        usuario = cursor.fetchone()
    conexion.close()
    return usuario

# Controlador para ver todos los municipios segun el departamento
def ObtenerMunicipios(id_departamento):
    conexion = obtener_conexion()
    municipios = []
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT m.MUN_ID, m.NOMBRE AS NOMBRE_MUNICIPIO
        FROM MUNICIPIO m
        WHERE m.DEPARTAMENTO_DEP_ID = %s""", (id_departamento, ))
        municipios = cursor.fetchall()
        municipios = [{"MUN_ID":municipio[0], "NOMBRE_MUNICIPIO":municipio[1]}for municipio in municipios]
    conexion.close()
    return municipios

# Controlador para ver todos los productos segun la empresa
def ObtenerProductosEmpresa(id_empresa):
    conexion = obtener_conexion()
    productos_empresa = []
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT p.PRO_ID, p.NOMBRE AS NOMBRE_PRODUCTO, p.DESCRIPCION, p.PRECIO, p.STOCK,
        p.FOTOGRAFIA, tp.T_PRO_ID, tp.NOMBRE AS NOMBRE_TIPO_PRODUCTO
        FROM PRODUCTO p
        INNER JOIN TIPO_PRODUCTO tp ON tp.T_PRO_ID = p.TIPO_PRODUCTO_T_PRO_ID
        WHERE p.EMPRESA_EMP_ID = %s""", (id_empresa, ))
        productos_empresa = cursor.fetchall()
        productos_empresa = [{"PRO_ID":producto[0], "NOMBRE_PRODUCTO":producto[1], "DESCRIPCION":producto[2], "PRECIO":producto[3], "STOCK":producto[4], "FOTOGRAFIA":producto[5], "T_PRO_ID":producto[6], "NOMBRE_TIPO_PRODUCTO":producto[7]}for producto in productos_empresa]
    conexion.close()
    return productos_empresa

# Controlador para ver todos los productos segun la empresa y segun el tipo de producto
def ObtenerProductosEmpresaTipoProducto(id_empresa, id_tipo_producto):
    conexion = obtener_conexion()
    productos_empresa = []
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT p.PRO_ID, p.NOMBRE AS NOMBRE_PRODUCTO, p.DESCRIPCION, p.PRECIO, p.STOCK,
        p.FOTOGRAFIA, tp.T_PRO_ID, tp.NOMBRE AS NOMBRE_TIPO_PRODUCTO
        FROM PRODUCTO p
        INNER JOIN TIPO_PRODUCTO tp ON tp.T_PRO_ID = p.TIPO_PRODUCTO_T_PRO_ID
        WHERE p.EMPRESA_EMP_ID = %s AND p.TIPO_PRODUCTO_T_PRO_ID = %s""", (id_empresa, id_tipo_producto, ))
        productos_empresa = cursor.fetchall()
        productos_empresa = [{"PRO_ID":producto[0], "NOMBRE_PRODUCTO":producto[1], "DESCRIPCION":producto[2], "PRECIO":producto[3], "STOCK":producto[4], "FOTOGRAFIA":producto[5], "T_PRO_ID":producto[6], "NOMBRE_TIPO_PRODUCTO":producto[7]}for producto in productos_empresa]
    conexion.close()
    return productos_empresa

# Controlador para agregar una direccion a la base de datos
def AgregarDireccion(id_municipio, lugar):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO DIRECCION(MUNICIPIO_MUN_ID, LUGAR) VALUES (%s, %s)",
                       (id_municipio, lugar))
        direccion_id = cursor.lastrowid
    conexion.commit()
    conexion.close()
    return direccion_id

# Controlador para insertar una empresa en la base de datos
def AgregarEmpresa(id_direccion, id_tipo_empresa, nombre, descripcion, correo, telefono, usuario, contrasenia, nit, nombre_archivo):
    conexion = obtener_conexion()
    password_encriptado = generate_password_hash(contrasenia, "sha256", 30)
    with conexion.cursor() as cursor:
        cursor.execute("""INSERT INTO EMPRESA (DIRECCION_DIR_ID, TIPO_EMPRESA_T_EMP_ID, NOMBRE, DESCRIPCION,
        CORREO, TELEFONO, USUARIO, CONTRASENA, NIT, ESTADO, DOCUMENTO)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (id_direccion, id_tipo_empresa, nombre, descripcion, correo, telefono, usuario, password_encriptado, nit, "pendiente", nombre_archivo))
        empresa_id = cursor.lastrowid
    conexion.commit()
    conexion.close()
    return empresa_id

# Controlador para insertar una solicitud en la base de datos
def AgregarSolicitud(id_empresa, id_repartidor, tipo_solicitud, fecha, descripcion, estado):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""INSERT INTO SOLICITUD
        (EMPRESA_EMP_ID, REPARTIDOR_REP_ID, TIPO_SOLICITUD, FECHA, DESCRIPCION, ESTADO)
        VALUES(%s, %s, %s, %s, %s, %s)""",
        (id_empresa, id_repartidor, tipo_solicitud, fecha, descripcion, estado))
    conexion.commit()
    conexion.close()

# Controlador para insertar un combo en la base de datos
def CrearCombo(nombre, descripcion, precio, nombre_archivo):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""INSERT INTO COMBO (NOMBRE, DESCRIPCION, PRECIO, FOTOGRAFIA)
        VALUES(%s, %s, %s, %s)""", (nombre, descripcion, precio, nombre_archivo))
    conexion.commit()
    conexion.close()

# Controlador para insertar un combo en la base de datos
def AgregarProductoACombo(id_combo, id_producto, cantidad, observaciones):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""INSERT INTO DETALLE_COMBO (COMBO_COM_ID, PRODUCTO_PRO_ID, CANTIDAD, OBSERVACIONES)
        VALUES(%s, %s, %s, %s)""", (id_combo, id_producto, cantidad, observaciones))
    conexion.commit()
    conexion.close()

# Controlador que se encarga de obtener los id de los productos que estan enlazados a un combo
def ObtenerProductoCombo(id_combo):
    conexion = obtener_conexion()
    ids_producto = []
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT PRODUCTO_PRO_ID FROM DETALLE_COMBO dc WHERE COMBO_COM_ID = %s""", (id_combo, ))
        ids_producto = cursor.fetchall()
    conexion.close()
    return ids_producto

# Controlador el cual obtiene toda la informacion que posee un combo
def ObtenerCombo(id_combo):
    conexion = obtener_conexion()
    combos = []
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT NOMBRE, DESCRIPCION, PRECIO, FOTOGRAFIA FROM COMBO c WHERE COM_ID = %s""", (id_combo, ))
        combos = cursor.fetchall()
        if combos:
            combos = [{"NOMBRE":combo[0], "DESCRIPCION":combo[1], "PRECIO":combo[2], "FOTOGRAFIA":combo[3]}for combo in combos]
        else:
            combos = None            
    conexion.close()
    return combos

# Controlador para eliminar una empresa en la base de datos
def EliminarEmpresa(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM EMPRESA WHERE EMP_ID = %s", (id,))
    conexion.commit()
    conexion.close()

# Controlador para eliminar un producto segun su id
def EliminarProducto(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM PRODUCTO WHERE PRO_ID = %s", (id,))
    conexion.commit()
    conexion.close()

# Controlador para eliminar un combo segun su id
def EliminarCombo(id_combo):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM COMBO WHERE COM_ID = %s", (id_combo,))
    conexion.commit()
    conexion.close()

# Controlador para eliminar el detalle de un combo segun el id del combo
def EliminarDetalleCombo(id_combo):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM DETALLE_COMBO WHERE COMBO_COM_ID = %s", (id_combo,))
    conexion.commit()
    conexion.close()

# Controlador para insertar un producto en la base de datos
def AgregarProducto(id_empresa, id_tipo_producto, nombre, descripcion, precio, stock, nombre_archivo):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""INSERT INTO PRODUCTO
        (EMPRESA_EMP_ID, TIPO_PRODUCTO_T_PRO_ID, NOMBRE, DESCRIPCION, PRECIO, STOCK, FOTOGRAFIA)
        VALUES(%s, %s, %s, %s, %s, %s, %s)""",
        (id_empresa, id_tipo_producto, nombre, descripcion, precio, stock, nombre_archivo))
    conexion.commit()
    conexion.close()

# Controlador para verificar los datos del admin en la base de datos
def VerificarSesAdmin(usuario, contrasenia):
    conexion = obtener_conexion()
    usuariosend = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM ADMINISTRADOR WHERE USUARIO = %s and CONTRASENA = %s", (usuario,contrasenia,))
        usuariosend = cursor.fetchone()
    conexion.close()
    return usuariosend

# Controlador para verificar los datos de un proveedor en la base de datos
def VerificarSesProveedor(usuario, contrasenia):
    conexion = obtener_conexion()
    proveedor = None
    with conexion.cursor() as cursor:
        cursor.execute("select * from (((REPARTIDOR inner JOIN DIRECCION ON REPARTIDOR.DIRECCION_DIR_ID = DIRECCION.DIR_ID)INNER JOIN MUNICIPIO ON MUNICIPIO.MUN_ID = DIRECCION.MUNICIPIO_MUN_ID) INNER JOIN DEPARTAMENTO ON DEPARTAMENTO.DEP_ID = MUNICIPIO.DEPARTAMENTO_DEP_ID) WHERE USUARIO = %s and CONTRASENA = %s", (usuario,contrasenia,))
        proveedor = cursor.fetchone()
    conexion.close()
    return {'REP_ID':proveedor[0],"DIRECCION_DIR_ID":proveedor[1],"NOMBRE":proveedor[2], "APELLIDO":proveedor[3],"CORREO":proveedor[4], "TELEFONO":proveedor[5], "USUARIO":proveedor[6], "CONTRASENA":proveedor[7], "NIT":proveedor[8],
        "ESTADO":proveedor[9],"DOCUMENTO":proveedor[10],"LICENCIA":proveedor[11], "TRANSPORTE":proveedor[12],"MUNICIPIO_MUN_ID": proveedor[14], "LUGAR":proveedor[15], "MUNICIPIO_NOMBRE":proveedor[18], "DEPARTAMENTO_ID": proveedor[19], "DEPARTAMENTO_NOMBRE":proveedor[20]}

def RegistrarRepartidor(nombre, apellido, usuario, contra, correo, telefono, nit, id_dep, id_muni, lugar, licencia, transporte, documento):
    conexion = obtener_conexion()
    password_encriptado = generate_password_hash(contra, "sha256", 30)
    id_direccion = ""
    id_repartidor = None 
    with conexion.cursor() as cursor:
        cursor.execute("CALL CrearDireccion("+str(id_muni)+",'"+lugar+"',@DIR_ID);")
    with conexion.cursor() as cursor:
        cursor.execute("SELECT @DIR_ID;")
        id_direccion = cursor.fetchone()[0]
    with conexion.cursor() as cursor:
        cursor.execute('''INSERT INTO REPARTIDOR(DIRECCION_DIR_ID, NOMBRE, APELLIDO, CORREO, TELEFONO,USUARIO, CONTRASENA, NIT, ESTADO,DOCUMENTO,LICENCIA,TRANSPORTE)
                          VALUES ('''+ str(id_direccion) +",'"+ nombre+"','"+ apellido+"','"+ correo+"'," +  telefono+",'"+ usuario+"','"+ password_encriptado+"','"+ nit+"','"+ "pendiente"+"','"+ documento+"','"+ licencia+"','"+ transporte +"')")
        cursor.execute("SELECT LAST_INSERT_ID();")
        id_repartidor = cursor.fetchone()[0]
    conexion.commit()
    conexion.close()
    return id_repartidor

def ExistenciaUsuario(usuario, tabla):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM "+ tabla +" WHERE usuario = '"+ usuario+ "';")
        valor = cursor.fetchone()[0]
        if valor != 0:
            return True
        return False


def RegistrarCliente(nombre, apellido, usuario, contra, correo, telefono, nit, id_dep, id_muni, lugar, tarjeta):
    conexion = obtener_conexion()
    password_encriptado = generate_password_hash(contra, "sha256", 30)
    id_direccion = ""
    with conexion.cursor() as cursor:
        cursor.execute("CALL CrearDireccion("+str(id_muni)+",'"+lugar+"',@DIR_ID);")
    with conexion.cursor() as cursor:
        cursor.execute("SELECT @DIR_ID;")
        id_direccion = cursor.fetchone()[0]
    with conexion.cursor() as cursor:
        cursor.execute('''INSERT INTO CLIENTE(DIRECCION_DIR_ID, NOMBRE, APELLIDO, CORREO, TELEFONO,USUARIO, CONTRASENA, NIT, TARJETA, ESTADO)
                          VALUES ('''+ str(id_direccion) +",'"+ nombre+"','"+ apellido+"','"+ correo+"'," +  telefono+",'"+ usuario+"','"+ password_encriptado+"','"+ nit+"','"+ tarjeta +"','"+"activo"+"')")
    conexion.commit()
    conexion.close()

# Controlador para actualizar un producto en la base de datos
def ActualizarProducto(id_producto, id_tipo_producto, nombre, descripcion, precio, stock, nombre_archivo):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""UPDATE proyecto_db.PRODUCTO
        SET TIPO_PRODUCTO_T_PRO_ID=%s, NOMBRE=%s, DESCRIPCION=%s, PRECIO=%s, STOCK=%s, FOTOGRAFIA=%s
        WHERE PRO_ID=%s""",
        (id_tipo_producto, nombre, descripcion, precio, stock, nombre_archivo, id_producto))
    conexion.commit()
    conexion.close()


def UltimaEmpresa():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT MAX(EMP_ID) FROM EMPRESA")
        id = cursor.fetchone()[0]
    conexion.close()
    return id

# Controlador para ver obtener una lista de empresas
def ObtenerEmpresas():
    conexion = obtener_conexion()
    empresaslist = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM EMPRESA")
        empresaslist = cursor.fetchall()
    conexion.close()
    return [{"EMP_ID":empresas[0], "DIRECCION_DIR_ID":empresas[1], "TIPO_EMPRESA_T_EMP_ID":empresas[2],
"NOMBRE":empresas[3], "DESCRIPCION":empresas[4], "CORREO":empresas[5], "TELEFONO":empresas[6], "USUARIO":empresas[7],
"CONTRASENA":empresas[8], "ESTADO":empresas[9],"NIT":empresas[10], "DOCUMENTO":empresas[11]}for empresas in empresaslist]
