from types import new_class

from mysql.connector import OperationalError
from conexion import obtener_conexion
from werkzeug.security import check_password_hash, generate_password_hash
import json

# Controlador para buscar un cliente en la base de datos
def LoguearCliente(nombre_usuario, contrasenia):
    conexion = obtener_conexion()
    usuario = None
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT c.CONTRASENA, c.CLI_ID, c.NOMBRE, c.APELLIDO, c.CORREO, c.TELEFONO, c.USUARIO, c.NIT, c.TARJETA, c.ESTADO, d.DIR_ID, d.LUGAR
                FROM CLIENTE c
                INNER JOIN DIRECCION d ON d.DIR_ID = c.DIRECCION_DIR_ID
                WHERE USUARIO = %s AND ESTADO = 'ACEPTADO'
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
            INNER JOIN DIRECCION d ON d.DIR_ID = e.DIRECCION_DIR_ID  WHERE USUARIO = %s AND ESTADO = 'ACEPTADO'""", (nombre_empresa,))
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
        (id_direccion, id_tipo_empresa, nombre, descripcion, correo, telefono, usuario, password_encriptado, nit, "PENDIENTE", nombre_archivo))
        empresa_id = cursor.lastrowid
    conexion.commit()
    conexion.close()
    return empresa_id

# Controlador para insertar una solicitud en la base de datos
def AgregarSolicitud(id_empresa, id_repartidor,id_dir, tipo_solicitud, fecha, descripcion, estado):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""INSERT INTO SOLICITUD
        (EMPRESA_EMP_ID, REPARTIDOR_REP_ID, DIRECCION_DIR_ID, TIPO_SOLICITUD, FECHA, DESCRIPCION, ESTADO)
        VALUES(%s, %s, %s, %s, %s, %s, %s)""",
        (id_empresa, id_repartidor, id_dir, tipo_solicitud, fecha, descripcion, estado))
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

# Controlador el cual obtiene toda la informacion que posee un combo como tambien su detalle
def MostrarCombosConProductos(id_empresa):
    conexion = obtener_conexion()
    combos = []
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT c.*, JSON_ARRAYAGG(JSON_OBJECT('id_producto', p.PRO_ID,'nombre', p.NOMBRE, 'cantidad', dc.CANTIDAD, 'observaciones', dc.OBSERVACIONES)) as detalle_combo
        FROM DETALLE_COMBO dc 
        INNER JOIN COMBO c ON c.COM_ID = dc.COMBO_COM_ID 
        INNER JOIN PRODUCTO p ON p.PRO_ID = dc.PRODUCTO_PRO_ID 
        WHERE p.EMPRESA_EMP_ID = %s
        GROUP BY c.COM_ID""", (id_empresa, ))
        combos = cursor.fetchall()
        
        if combos:
            combos = [{"ID_COMBO":combo[0], "NOMBRE":combo[1], "DESCRIPCION":combo[2], "PRECIO":combo[3], "FOTOGRAFIA":combo[4], "DETALLE_COMBO":json.loads(combo[5])}for combo in combos]
        else:
            combos = None
    conexion.close()
    return combos

# Controlador el cual obtiene toda la informacion que posee una orden como tambien su detalle
def MostrarOrdenes(id_empresa):
    conexion = obtener_conexion()
    combos = []
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT o.ORD_ID, c.CLI_ID, CONCAT(c.NOMBRE, ', ', c.APELLIDO) AS NOMBRE_COMPLETO_CLIENTE, d.LUGAR, o.FECHA, o.ESTADO,
        JSON_ARRAYAGG(JSON_OBJECT(
        'ID_ARTICULO', CASE WHEN c2.COM_ID IS NULL THEN p.PRO_ID ELSE c2.COM_ID END, 
        'NOMBRE_ARTICULO', CASE WHEN c2.NOMBRE IS NULL THEN p.NOMBRE ELSE c2.NOMBRE END, 
        'PRECIO_ARTICULO', CASE WHEN c2.PRECIO IS NULL THEN p.PRECIO ELSE c2.PRECIO END,
        'ES_COMBO', CASE WHEN c2.COM_ID IS NULL THEN FALSE ELSE TRUE END
        ))
        FROM ORDEN o
        INNER JOIN CLIENTE c ON c.CLI_ID = o.CLIENTE_CLI_ID 
        INNER JOIN DIRECCION d ON d.DIR_ID = o.DIRECCION_DIR_ID 
        INNER JOIN DETALLE_ORDEN do ON do.ORDEN_ORD_ID = o.ORD_ID
        LEFT JOIN COMBO c2 ON c2.COM_ID = do.COMBO_COM_ID 
        LEFT JOIN PRODUCTO p ON p.PRO_ID = do.PRODUCTO_PRO_ID  
        WHERE (p.EMPRESA_EMP_ID = %s OR c2.COM_ID IN (SELECT COMBO_COM_ID FROM DETALLE_COMBO dc 
        INNER JOIN PRODUCTO p ON p.PRO_ID = dc.PRODUCTO_PRO_ID
        WHERE p.EMPRESA_EMP_ID = %s)) AND o.ESTADO = 'PENDIENTE' AND do.ESTADO = 'PENDIENTE'
        GROUP BY o.ORD_ID""", (id_empresa, id_empresa ))
        combos = cursor.fetchall()
        
        if combos:
            combos = [{"ORD_ID":combo[0], "CLI_ID":combo[1], "NOMBRE_COMPLETO_CLIENTE":combo[2], "LUGAR":combo[3], "FECHA": combo[4], "ESTADO": combo[5], "DETALLE_ORDEN":json.loads(combo[6])}for combo in combos]
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


def VerificarSesRepartidor(usuario, contraseña):
    conexion = obtener_conexion()
    usuariosend = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM REPARTIDOR WHERE USUARIO = %s and ESTADO = 'ACEPTADO'", (usuario,))
        usuariosend = cursor.fetchone()
        if not(usuariosend and check_password_hash(usuariosend[7], contraseña)):
            usuariosend = None
    conexion.close()
    return usuariosend



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
                          VALUES ('''+ str(id_direccion) +",'"+ nombre+"','"+ apellido+"','"+ correo+"'," +  telefono+",'"+ usuario+"','"+ password_encriptado+"','"+ nit+"','"+ "PENDIENTE"+"','"+ documento+"','"+ licencia+"','"+ transporte +"')")
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
                          VALUES ('''+ str(id_direccion) +",'"+ nombre+"','"+ apellido+"','"+ correo+"'," +  telefono+",'"+ usuario+"','"+ password_encriptado+"','"+ nit+"','"+ tarjeta +"','"+"ACEPTADO"+"')")
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

# Controlador para actualizar un estado de un detalle orden
def ActualizarEstadoDetalleOrden(id_orden, id_combo, id_producto, estado):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        if id_combo == "" and id_producto != "":
            cursor.execute("""UPDATE DETALLE_ORDEN 
            SET ESTADO = %s WHERE ORDEN_ORD_ID = %s AND PRODUCTO_PRO_ID = %s AND COMBO_COM_ID IS NULL""",
            (estado, id_orden, id_producto))
        elif id_combo != "" and id_producto == "":
            cursor.execute("""UPDATE DETALLE_ORDEN 
            SET ESTADO = %s WHERE ORDEN_ORD_ID = %s AND PRODUCTO_PRO_ID IS NULL AND COMBO_COM_ID = %s""",
            (estado, id_orden, id_combo))
        cursor.execute("""call ActualizarEstadoOrden(%s)""",(id_orden,))
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

# Controlador para ver obtener una lista de combos con sus datos
def ObtenerlistaCombosEmpresa(id_empresa):
    conexion = obtener_conexion()
    listacombos = []
    with conexion.cursor() as cursor:
        cursor.execute("select DISTINCT COMBO_COM_ID, COMBO.NOMBRE AS NOMBRE_COMBO, COMBO.DESCRIPCION AS DESCRIPCION_COMBO, COMBO.PRECIO AS PRECIO_COMBO, COMBO.FOTOGRAFIA AS FOTOGRAFIA_COMBO  from ((DETALLE_COMBO inner join COMBO on DETALLE_COMBO.COMBO_COM_ID = COMBO.COM_ID )INNER JOIN PRODUCTO ON PRODUCTO.PRO_ID = DETALLE_COMBO.PRODUCTO_PRO_ID) where PRODUCTO.EMPRESA_EMP_ID = %s;", (id_empresa,))
        combos = cursor.fetchall()
        for combo in combos:
            
            cursor.execute("select PRODUCTO_PRO_ID, EMPRESA_EMP_ID, TIPO_PRODUCTO_T_PRO_ID, PRODUCTO.NOMBRE, PRODUCTO.DESCRIPCION, PRODUCTO.PRECIO, STOCK, PRODUCTO.FOTOGRAFIA, CANTIDAD, OBSERVACIONES from ((DETALLE_COMBO inner join COMBO on DETALLE_COMBO.COMBO_COM_ID = COMBO.COM_ID )INNER JOIN PRODUCTO ON PRODUCTO.PRO_ID = DETALLE_COMBO.PRODUCTO_PRO_ID) where COMBO.COM_ID = %s;", (combo[0],))             
            productos = cursor.fetchall()       
            listaproductos = []
            for producto in productos:
                newproducto = {"PRODUCTO_PRO_ID": producto[0], "EMPRESA_EMP_ID": producto[1], "TIPO_PRODUCTO_T_PRO_ID": producto[2], "NOMBRE": producto[3], "DESCRIPCION": producto[4], "PRECIO": producto[5], "STOCK": producto[6], "FOTOGRAFIA": producto[7], "CANTIDAD": producto[8], "OBSERVACIONES": producto[9]}
                listaproductos.append(newproducto)
                
            newcombo = {"COMBO_COM_ID": combo[0], "NOMBRE_COMBO": combo[1], "DESCRIPCION_COMBO": combo[2], "PRECIO_COMBO": combo[3], "FOTOGRAFIA_COMBO": combo[4], "PRODUCTOS": listaproductos}
            listacombos.append(newcombo)
    conexion.close()
    return listacombos

# Controlador para eliminar producto del carrito
def EliminarProductoCarrito(id_producto, id_cliente):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT ORD_ID FROM ORDEN WHERE CLIENTE_CLI_ID = " + str(id_cliente) + " AND ESTADO = 'PENDIENTE';")
        IDCOMBO = cursor.fetchone()
        
        cursor.execute("DELETE FROM DETALLE_ORDEN WHERE PRODUCTO_PRO_ID = %s AND PRODUCTO_PRO_ID = %s;", (id_producto, IDCOMBO))
        
    conexion.commit()
    conexion.close()
    return True

# Controlador para eliminar producto del carrito
def EliminarComboCarrito(id_combo, id_cliente):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT ORD_ID FROM ORDEN WHERE CLIENTE_CLI_ID = " + str(id_cliente) + " AND ESTADO = 'PENDIENTE';")
        IDCOMBO = cursor.fetchone()
        
        cursor.execute("DELETE FROM DETALLE_ORDEN WHERE PRODUCTO_PRO_ID = %s AND COMBO_COM_ID = %s;", (id_combo, IDCOMBO))
        
    conexion.commit()
    conexion.close()
    return True

# Controlador para confirmar orden
def ConfirmarOrdenCarrito(id_cliente):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT ORD_ID FROM ORDEN WHERE CLIENTE_CLI_ID = " + str(id_cliente) + " AND ESTADO = 'PENDIENTE';")
        IDORDEN = cursor.fetchone()
        
        cursor.execute("UPDATE ORDEN SET ESTADO = 'PENDIENTE' WHERE ORD_ID = %s;", (IDORDEN))
        
    conexion.commit()
    conexion.close()
    return True


def AgregarDetalleOrden(id_combo, id_orden, cantidad, id_producto, observaciones, estado):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO DETALLE_ORDEN (COMBO_COM_ID, ORDEN_ORD_ID, PRODUCTO_PRO_ID, CANTIDAD, OBSERVACIONES,ESTADO)" + 
                          "VALUES (" + str(id_combo) + "," + str(id_orden) + "," + str(id_producto) + "," + str(cantidad) + ",'" + observaciones + "','" + "PENDIENTE" + "');")
    conexion.commit()
    conexion.close()


def CrearDireccion(id_municipio, lugar):
    conexion = obtener_conexion()
    id_direccion = None
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO DIRECCION (MUNICIPIO_MUN_ID, LUGAR)" + 
                       "VALUES (" + str(id_municipio) + ",'" + lugar + "');")
        cursor.execute("SELECT LAST_INSERT_ID();")
        id_direccion = cursor.fetchone()[0]
    conexion.commit()
    conexion.close()
    return id_direccion

def ActualizarTarjeta(id_cliente, tarjeta):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE CLIENTE SET TARJETA = %s WHERE CLI_ID = %s;", (tarjeta, id_cliente))
    conexion.commit()
    conexion.close()


def AgregarProductoCarrito(id_cliente, id_direccion, id_repartidor,fecha, calificacion, comentario, metodo_pago):
    conexion = obtener_conexion()
    id_orden = None
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO ORDEN (CLIENTE_CLI_ID, DIRECCION_DIR_ID, REPARTIDOR_REP_ID, FECHA, ESTADO, CALIFICACION, COMENTARIO, METODO_PAGO)" +
        "VALUES (" + str(id_cliente) + "," + str(id_direccion) + ",NULL , NOW(),'" + "PENDIENTE" + "','" + str(calificacion) + "','" + comentario + "','" + metodo_pago + "');")
        cursor.execute("SELECT LAST_INSERT_ID();")
        id_orden = cursor.fetchone()[0]
    conexion.commit()
    conexion.close()
    return id_orden



def MostrarCarrito(id_cliente):
    conexion = obtener_conexion()
    id_orden = None
    contenido = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT ORD_ID FROM ORDEN WHERE CLIENTE_CLI_ID = " + str(id_cliente) + " AND ESTADO = 'PENDIENTE';")
        id_orden = cursor.fetchone()[0]
    if id_orden is None:
        cursor.execute("select PRO_ID, EMPRESA_EMP_ID, NOMBRE, DESCRIPCION, PRECIO, STOCK, FOTOGRAFIA from ((ORDEN inner JOIN DETALLE_ORDEN ON DETALLE_ORDEN.COMBO_COM_ID = ORDEN.ORD_ID) INNER JOIN PRODUCTO ON PRODUCTO.PRO_ID = DETALLE_ORDEN.PRODUCTO_PRO_ID) where ORD_ID = %s;", (id_orden,))
        contenidofetch = cursor.fetchall()
        contenido = {"PRO_ID": contenidofetch[0], "EMPRESA_EMP_ID": contenidofetch[1], "NOMBRE": contenidofetch[2], "DESCRIPCION": contenidofetch[3], "PRECIO": contenidofetch[4], "STOCK": contenidofetch[5], "FOTOGRAFIA": contenidofetch[6]}
    return contenido

def MostrarCarritoCombos(id_cliente):
    conexion = obtener_conexion()
    id_orden = None
    contenido = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT ORD_ID FROM ORDEN WHERE CLIENTE_CLI_ID = " + str(id_cliente) + " AND ESTADO = 'PENDIENTE';")
        id_orden = cursor.fetchone()[0]
    if id_orden is None:
        cursor.execute("select COM_ID, NOMBRE, DESCRIPCION, PRECIO, FOTOGRAFIA from ((ORDEN inner JOIN DETALLE_ORDEN ON DETALLE_ORDEN.COMBO_COM_ID = ORDEN.ORD_ID) INNER JOIN COMBO ON COMBO.COM_ID = DETALLE_ORDEN.ORDEN_ORD_ID) where ORD_ID = %s;", (id_orden,))
        contenidofetch = cursor.fetchall()
        contenido = [{"COM_ID":combo[0],"NOMBRE": combo[1],"DESCRIPCION": combo[2], "PRECIO": combo[3], "FOTOGRAFIA":combo[4]}for combo in contenidofetch]
    return contenido
        
        
def MostrarProductosDeUnCombo(id_combo):
    conexion = obtener_conexion()    
    with conexion.cursor() as cursor:
        cursor.execute("select PRODUCTO_PRO_ID, EMPRESA_EMP_ID, TIPO_PRODUCTO_T_PRO_ID, PRODUCTO.NOMBRE, PRODUCTO.DESCRIPCION, PRODUCTO.PRECIO, STOCK, PRODUCTO.FOTOGRAFIA, CANTIDAD, OBSERVACIONES from ((DETALLE_COMBO inner join COMBO on DETALLE_COMBO.COMBO_COM_ID = COMBO.COM_ID )INNER JOIN PRODUCTO ON PRODUCTO.PRO_ID = DETALLE_COMBO.PRODUCTO_PRO_ID) where COMBO.COM_ID = %s;", (id_combo,))
        productos = cursor.fetchall()
        listaproductos = []
        for producto in productos:
            newproducto = {"PRODUCTO_PRO_ID": producto[0], "EMPRESA_EMP_ID": producto[1], "TIPO_PRODUCTO_T_PRO_ID": producto[2], "NOMBRE": producto[3], "DESCRIPCION": producto[4], "PRECIO": producto[5], "STOCK": producto[6], "FOTOGRAFIA": producto[7], "CANTIDAD": producto[8], "OBSERVACIONES": producto[9]}
            listaproductos.append(newproducto)
    return listaproductos  


def ModificarProductoCarrito(id_cliente, id_direccion, id_repartidor, fecha, calificacion, comentario, metodo_pago):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT ORD_ID FROM ORDEN WHERE CLIENTE_CLI_ID = " + str(id_cliente) + " AND ESTADO = 'PENDIENTE';")
        id_orden = cursor.fetchone()[0]
        cursor.execute("UPDATE ORDEN SET CLIENTE_CLI_ID = " + str(id_cliente) + ", DIRECCION_DIR_ID = " + str(id_direccion) + ", REPARTIDOR_REP_ID = " + str(id_repartidor) + ", FECHA = '" + fecha + "', CALIFICACION = " + str(calificacion) + ", COMENTARIO = '" + comentario + "', METODO_PAGO = '" + metodo_pago + "' WHERE ORD_ID = " + str(id_orden) + ";")
    conexion.commit()
    conexion.close()
    return id_orden

def ModificarComboCarrito(id_cliente, id_direccion, id_repartidor, fecha, calificacion, comentario, metodo_pago):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT ORD_ID FROM ORDEN WHERE CLIENTE_CLI_ID = " + str(id_cliente) + " AND ESTADO = 'PENDIENTE';")
        id_orden = cursor.fetchone()[0]
        cursor.execute("UPDATE ORDEN SET CLIENTE_CLI_ID = " + str(id_cliente) + ", DIRECCION_DIR_ID = " + str(id_direccion) + ", REPARTIDOR_REP_ID = " + str(id_repartidor) + ", FECHA = '" + fecha + "', CALIFICACION = " + str(calificacion) + ", COMENTARIO = '" + comentario + "', METODO_PAGO = '" + metodo_pago + "' WHERE ORD_ID = " + str(id_orden) + ";")
    conexion.commit()
    conexion.close()
    return id_orden


def ModificarDetalleOrdenCombo(id_orden, id_combo, cantidad, observaciones):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE DETALLE_ORDEN SET CANTIDAD = " + str(cantidad) + ", OBSERVACIONES = '" + observaciones + "' WHERE ORDEN_ORD_ID = " + str(id_orden) + " AND COMBO_COM_ID = " + str(id_combo) + ";")
    conexion.commit()
    conexion.close()

def ModificarDetalleOrdenProducto(id_orden, id_producto, cantidad, observaciones):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE DETALLE_ORDEN SET CANTIDAD = " + str(cantidad) + ", OBSERVACIONES = '" + observaciones + "' WHERE ORDEN_ORD_ID = " + str(id_orden) + " AND PRODUCTO_PRO_ID = " + str(id_producto) + ";")
    conexion.commit()
    conexion.close()

# Controlador para retornar los pedidos pendientes de asignacion de repartidor
def VerPedidosPendientesRepartidor(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
           SELECT o.ORD_ID, c.NOMBRE, c.APELLIDO, d2.NOMBRE, m.NOMBRE, d.LUGAR, o.METODO_PAGO, o.ESTADO  
            FROM ORDEN o 
            INNER JOIN CLIENTE c ON c.CLI_ID = o.CLIENTE_CLI_ID 
            INNER JOIN DIRECCION d ON d.DIR_ID = c.DIRECCION_DIR_ID
            INNER JOIN MUNICIPIO m ON d.MUNICIPIO_MUN_ID = m.MUN_ID 
            INNER JOIN DEPARTAMENTO d2 ON d2.DEP_ID = m.DEPARTAMENTO_DEP_ID
            INNER JOIN REPARTIDOR r ON r.REP_ID = %s 
            INNER JOIN DIRECCION r_d ON r_d.DIR_ID = r.DIRECCION_DIR_ID
            INNER JOIN MUNICIPIO r_m ON r_d.MUNICIPIO_MUN_ID = r_m.MUN_ID
            INNER JOIN DEPARTAMENTO r_d2 ON r_m.DEPARTAMENTO_DEP_ID = r_d2.DEP_ID
            WHERE o.ESTADO = 'RECIBIDO'
            and (r_m.MUN_ID = m.MUN_ID)
            and (r_d2.DEP_ID = d2.DEP_ID)""", (id,))
        pendientes = cursor.fetchall()
        print(pendientes)
        lista_pedidos = []
        for pedido in pendientes:
            new_pendiente = {"ORD_ID":pedido[0], "CLIENTE":pedido[1]+" "+pedido[2], "DEPARTAMENTO":pedido[3], "MUNICIPIO":pedido[4], "LUGAR":pedido[5], "METODO_PAGO":pedido[6], "ESTADO":pedido[7]}
            lista_pedidos.append(new_pendiente)
        conexion.close()
        return lista_pedidos

#Controlador que retorna el id del usuario de tipo repartidor logeado.
def VerIdRepartidorLog(nombre):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT REP_ID FROM REPARTIDOR WHERE USUARIO ="+str(nombre))
        id_rep = cursor.fetchone()[0]
        conexion.close()
        return id_rep

#Controlador que retorna el id de la orden asignada al repartidor
def VerIdOrdenAsignadaRepartidor(rep_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT ORD_ID FROM ORDEN WHERE ESTADO = 'EN PROCESO' AND REPARTIDOR_REP_ID =%s",(rep_id,))
        id_ord = cursor.fetchone()
        conexion.close()
        if not id_ord: 
            raise Exception('No records')
        return id_ord 

#Controlador para retornar la orden asignada al repartidor
def VerPedidoAsignadoRepartidor(id_repartidor):
    conexion = obtener_conexion()
    print('test')
    with conexion.cursor() as cursor:
        id_ord = VerIdOrdenAsignadaRepartidor(id_repartidor)
        cursor.execute("""SELECT O.ORD_ID, C.NOMBRE, C.APELLIDO, D2.NOMBRE, M.NOMBRE, D.LUGAR, O.METODO_PAGO, O.ESTADO FROM ORDEN O
        INNER JOIN CLIENTE C on O.CLIENTE_CLI_ID = C.CLI_ID
        INNER JOIN DIRECCION D on O.DIRECCION_DIR_ID = D.DIR_ID
        INNER JOIN MUNICIPIO M on D.MUNICIPIO_MUN_ID = M.MUN_ID
        INNER JOIN DEPARTAMENTO D2 on M.DEPARTAMENTO_DEP_ID = D2.DEP_ID
        WHERE O.ESTADO = 'EN PROCESO' AND O.ORD_ID = %s""", id_ord)
        pedido = cursor.fetchone()
        if not pedido:
            raise Exception('No records')

        print('testing')
        cursor.execute("""SELECT COALESCE(C.NOMBRE, '') as nombre_combo, P.NOMBRE, D.CANTIDAD, D.OBSERVACIONES
            FROM DETALLE_ORDEN D
            LEFT JOIN COMBO C ON D.COMBO_COM_ID = C.COM_ID
            INNER JOIN PRODUCTO P ON D.PRODUCTO_PRO_ID = P.PRO_ID
            WHERE D.ORDEN_ORD_ID = %s""", id_ord)
        lista_p = []
        new_prod = None
        lista_productos = cursor.fetchall()
        print(lista_productos)
        for producto in lista_productos:
            if producto[0] != "":
                new_prod = {"DESCRIPCION":producto[0], "CANTIDAD":producto[2], "OBSERVACIONES": producto[3]}
                lista_p.append(new_prod)
            elif producto[1] != None:
                new_prod = {"DESCRIPCION":producto[1], "CANTIDAD":producto[2], "OBSERVACIONES": producto[3]}
                lista_p.append(new_prod)
        asignado = {"ORD_ID":pedido[0],"CLIENTE":pedido[1]+" "+pedido[2], "DEPARTAMENTO":pedido[3], "MUNICIPIO":pedido[4], "LUGAR":pedido[5], "METODO_PAGO":pedido[6], "ESTADO":pedido[7], "PRODUCTOS":lista_p}
        return asignado
    
#Controlador para cambiar el estado del producto asignado
def AsignarPedidoRepartidor(id_ord, usuario_rep):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.callproc("AsignarPedidoRepartidor", (id_ord, usuario_rep,))
        conexion.commit()
        conexion.close()

#Controlador para cambiar el estado del pedido a "entregado" 
def EntregarPedidoRepartidor(ord_id, usuario):
    print('ord_id ', ord_id)
    print('rep ', usuario)
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""UPDATE ORDEN O
        INNER JOIN REPARTIDOR R on O.REPARTIDOR_REP_ID = R.REP_ID
        SET O.ESTADO = 'ENTREGADO'
        WHERE O.ESTADO = 'EN PROCESO' AND O.ORD_ID=%s AND R.REP_ID = %s;""", (ord_id, usuario,))
        conexion.commit()

        conexion.close()

def VerTiposProductos():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM TIPO_PRODUCTO;")
        tipos = cursor.fetchall()
        lista_tipos = []
        for tipo in tipos:
            new_tipo = {"T_PRO_ID":tipo[0], "NOMBRE":tipo[1]}
            lista_tipos.append(new_tipo)
        conexion.close()
        return lista_tipos
    
def VerEmpresasPorTipo(tipo):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM EMPRESA WHERE TIPO_EMPRESA_T_EMP_ID = "+str(tipo))
        empresas = cursor.fetchall()
        lista_empresas = []
        for empresa in empresas:
            new_empresa = {"EMP_ID":empresa[0],"DIR_ID":empresa[1], "T_EMP_ID":empresa[2], "NOMBRE":empresa[3], "DESCRIPCION":empresa[4], "CORREO":empresa[5], "TELEFONO":empresa[6], "USUARIO":empresa[7], "CONTRASENA":empresa[8], "NIT":empresa[9], "ESTADO":empresa[10], "DOCUMENTO":empresa[11]}
            lista_empresas.append(new_empresa)
        conexion.close()
        return lista_empresas

def VerCombosPorProducto(producto_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = """SELECT c.COM_ID, c.NOMBRE, c.DESCRIPCION, c.PRECIO, c.FOTOGRAFIA, dc.CANTIDAD, dc.OBSERVACIONES, p.PRO_ID, p.NOMBRE
                 FROM COMBO c
                 JOIN DETALLE_COMBO dc ON c.COM_ID = dc.COMBO_COM_ID
                 JOIN PRODUCTO p ON dc.PRODUCTO_PRO_ID = p.PRO_ID
                 WHERE p.PRO_ID = %s"""
        cursor.execute(sql, (producto_id,))
        combos = cursor.fetchall()
        lista_combos = []
        combo_temp = {}
        for combo in combos:
            if combo_temp.get('ID_COMBO') != combo[0]:
                if combo_temp:
                    lista_combos.append(combo_temp)
                combo_temp = {"ID_COMBO": combo[0],
                              "NOMBRE": combo[1],
                              "DESCRIPCION": combo[2],
                              "PRECIO": combo[3],
                              "FOTOGRAFIA": combo[4],
                              "DETALLE_COMBO": []}
            detalle_temp = {"id_producto": combo[7],
                            "nombre": combo[8],
                            "cantidad": combo[5],
                            "observaciones": combo[6]}
            combo_temp["DETALLE_COMBO"].append(detalle_temp)
        lista_combos.append(combo_temp)
        conexion.close()
        return lista_combos

#Controlador para ver los combos por el tipo del producto
def VerCombosPorTipo(tipo):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = """SELECT DISTINCT c.COM_ID, c.NOMBRE, c.DESCRIPCION, c.PRECIO, c.FOTOGRAFIA
                 FROM COMBO c
                 JOIN DETALLE_COMBO dc ON c.COM_ID = dc.COMBO_COM_ID
                 JOIN PRODUCTO p ON dc.PRODUCTO_PRO_ID = p.PRO_ID
                 JOIN TIPO_PRODUCTO tp ON p.TIPO_PRODUCTO_T_PRO_ID = tp.T_PRO_ID
                 WHERE tp.T_PRO_ID = %s"""
        cursor.execute(sql, (tipo,))
        combos = cursor.fetchall()
        lista_combos = [{"COM_ID": combo[0], "NOMBRE": combo[1], "DESCRIPCION": combo[2], "PRECIO": combo[3], "FOTOGRAFIA": combo[4]} for combo in combos]        
        conexion.close()
        return lista_combos
    
#Controlador para ver el perfil del repartidor logueado
def VerPerfilRepartidor(usuario, mes):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT R.NOMBRE, R.APELLIDO, R.USUARIO, R.CORREO, R.NIT, D2.DEP_ID, M.MUN_ID, D.LUGAR, R.LICENCIA, R.TRANSPORTE, R.DOCUMENTO, R.TELEFONO FROM REPARTIDOR R
        INNER JOIN DIRECCION D on R.DIRECCION_DIR_ID = D.DIR_ID
        INNER JOIN MUNICIPIO M on D.MUNICIPIO_MUN_ID = M.MUN_ID
        INNER JOIN DEPARTAMENTO D2 on M.DEPARTAMENTO_DEP_ID = D2.DEP_ID
        WHERE R.REP_ID =%s """,(usuario,))
        logueado = cursor.fetchone()
        calificacion = VerCalificacionPromedioRepartidor(usuario, mes)
        comision = VerComisionRepartidor(usuario, mes)
        new_user = {"NOMBRE":logueado[0], "APELLIDO":logueado[1], "USUARIO":logueado[2], "CORREO":logueado[3], "NIT":logueado[4], "ID_DEP":logueado[5], "ID_MUNI":logueado[6], "LUGAR":logueado[7], "LICENCIA":logueado[8], "TRANSPORTE":logueado[9],"DOCUMENTO":logueado[10],"TELEFONO": logueado[11], "CALIFICACION":calificacion, "COMISION":comision}
        conexion.close()
        return new_user
       
#Controlador que retorna la calificacion promedio en el mes del repartidor logueado
def VerCalificacionPromedioRepartidor(usuario, mes):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT AVG(O.CALIFICACION) FROM ORDEN O
        INNER JOIN REPARTIDOR R on O.REPARTIDOR_REP_ID = R.REP_ID
        WHERE R.REP_ID = %s AND MONTH(O.FECHA) = %s;""",(usuario,mes,))
        valor = cursor.fetchone()
        conexion.close()
        if valor[0] == None:
            return 0
        return valor[0]
    
#Controlador para ver las comisiones generadas en el mes del repartidor logueado
def VerComisionRepartidor(usuario, mes):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT SUM(V.TOTAL)*0.05 AS COMISION FROM VENTA V
        INNER JOIN ORDEN O on V.ORDEN_ORD_ID = O.ORD_ID
        INNER JOIN REPARTIDOR R on O.REPARTIDOR_REP_ID = R.REP_ID
        WHERE R.REP_ID =%s AND MONTH(V.FECHA) = %s""", (usuario, mes,)) 
        valor = cursor.fetchone()
        conexion.close()
        if valor[0]: 
            return valor[0]
        else: 
            return 0 

def VerOrdenesCliente(id_cliente):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT O.ORD_ID, O.FECHA, O.ESTADO, O.METODO_PAGO, O.CALIFICACION, O.COMENTARIO, O.CLIENTE_CLI_ID, R.NOMBRE AS NOMBRE_REPARTIDOR, D.LUGAR
                        FROM ORDEN O
                        INNER JOIN CLIENTE C ON O.CLIENTE_CLI_ID = C.CLI_ID
                        INNER JOIN REPARTIDOR R ON O.REPARTIDOR_REP_ID = R.REP_ID
                        INNER JOIN DIRECCION D ON O.DIRECCION_DIR_ID = D.DIR_ID
                        WHERE C.CLI_ID =  %s;""",(id_cliente,))
        ordenes = cursor.fetchall()
        lista_ordenes = [{"ORD_ID": orden[0], "FECHA": orden[1], "ESTADO": orden[2], "METODO_PAGO": orden[3], "CALIFICACION": orden[4], "COMENTARIO": orden[5], "CLIENTE_CLI_ID": orden[6], "NOMBRE_REPARTIDOR": orden[7], "LUGAR": orden[8]} for orden in ordenes]
        conexion.close()
        return lista_ordenes
    
#Controlador para actualizar el comentario y la calificacion de una orden
def ActualizarOrden(id_orden, comentario, calificacion):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""UPDATE ORDEN SET CALIFICACION = %s, COMENTARIO = %s WHERE ORD_ID = %s;""",(calificacion, comentario, id_orden))
        conexion.commit()
        conexion.close()
        return True
    
    #Controlador para actualizar los datos del repartidor
def ActualizarPerfilRepartidor(correo,contrasena, nit, telefono, transporte, licencia,usuario):
    conexion = obtener_conexion()

    with conexion.cursor() as cursor:
        if contrasena:
            password_encriptado = generate_password_hash(contrasena, "sha256", 30)
            query = """UPDATE REPARTIDOR R
            SET R.CORREO = %s,
            R.CONTRASENA = %s,
            R.NIT = %s,
            R.TELEFONO = %s,
            R.TRANSPORTE = %s,
            R.LICENCIA =%s
            WHERE R.USUARIO =%s""" 
            cursor.execute(query,(correo,password_encriptado, nit, telefono, transporte, licencia,usuario,))
            conexion.commit()
        else:
            query = """UPDATE REPARTIDOR R
            SET CORREO = %s,
            NIT = %s,
            TELEFONO = %s,
            TRANSPORTE = %s,
            LICENCIA =%s
            WHERE USUARIO = %s"""
            cursor.execute(query,(correo, nit, telefono, transporte, licencia,usuario,))
            conexion.commit()

        conexion.close()

#Controlador para ver todos los pedidos entregados por el repartidor con sesion activa
def VerPedidosEntregadosRepartidor(usuario):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT O.ORD_ID, C.NOMBRE, C.APELLIDO, D2.NOMBRE, M.NOMBRE, D.LUGAR, O.FECHA, O.METODO_PAGO, O.ESTADO FROM ORDEN O
        INNER JOIN CLIENTE C on O.CLIENTE_CLI_ID = C.CLI_ID
        INNER JOIN DIRECCION D on C.DIRECCION_DIR_ID = D.DIR_ID
        INNER JOIN MUNICIPIO M on D.MUNICIPIO_MUN_ID = M.MUN_ID
        INNER JOIN DEPARTAMENTO D2 on M.DEPARTAMENTO_DEP_ID = D2.DEP_ID
        INNER JOIN REPARTIDOR R on O.REPARTIDOR_REP_ID = R.REP_ID
        WHERE R.USUARIO = %s AND O.ESTADO = 'ENTREGADO';""", (usuario,))
        pedidos = cursor.fetchall()
        lista_pedidos = []
        for pedido in pedidos:
            new_pedido = {"ORD_ID":pedido[0],"NOMBRE_CLIENTE":pedido[1], "APELLIDO_CLIENTE":pedido[2], "DEPARTAMENTO":pedido[3], "MUNICIPIO":pedido[4],"LUGAR":pedido[5], "FECHA":pedido[6], "METODO_PAGO":pedido[7],"ESTADO":pedido[8]}
            lista_pedidos.append(new_pedido)
        conexion.close()
        return lista_pedidos

def ActualizarComentarioCalificacion(id_orden, comentario, calificacion):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""UPDATE ORDEN SET COMENTARIO = %s, CALIFICACION = %s WHERE ORD_ID = %s;""",(comentario, calificacion, id_orden))
        conexion.commit()
        conexion.close() 


#Controlador para deshabilitar un usuario de tipo repartidor
def DeshabilitarRepartidor(id_rep):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""UPDATE REPARTIDOR R SET R.ESTADO = 'RECHAZADO' WHERE R.REP_ID = %s;""",(id_rep,))
        conexion.commit()
        conexion.close()


#Controlador para deshabilitar un usuario de tipo empresa 
def DeshabilitarEmpresa(id_emp):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""UPDATE EMPRESA E SET E.ESTADO = 'RECHAZADO' WHERE E.EMP_ID = %s;""",(id_emp,))
        conexion.commit()
        conexion.close()

#Controlador para deshabilitar un usuario de tipo cliente
def DeshabilitarCliente(id_cli):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""UPDATE CLIENTE C SET C.ESTADO = 'RECHAZADO' WHERE C.CLI_ID = %s;""",(id_cli,))
        conexion.commit()
        conexion.close()

        
def VerUltimoComboInsertado():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT * FROM COMBO
ORDER BY COM_ID desc limit 1;""")
        valor = cursor.fetchone()
        conexion.close()
        return {"COM_ID":valor[0], "NOMBRE":valor[1], "DESCRIPCION":valor[2], "PRECIO":valor[3], "FOTO":valor[4] }

#Controlador para ver todos las empresas en estado ACEPTADO para poder deshabilitarlo
def VerEmpresasAdmin():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT E.EMP_ID, E.NOMBRE, E.USUARIO, E.CONTRASENA, E.DESCRIPCION, TE.NOMBRE, E.CORREO, E.TELEFONO, E.NIT FROM EMPRESA E
        INNER JOIN TIPO_EMPRESA TE on E.TIPO_EMPRESA_T_EMP_ID = TE.T_EMP_ID
        WHERE E.ESTADO = 'ACEPTADO';""")
        lista_empresas = []
        empresas = cursor.fetchall()
        for empresa in empresas:
            new_empresa = {"EMP_ID":empresa[0], "NOMBRE":empresa[1], "USUARIO":empresa[2], "CONTRASENA":empresa[3], "DESCRIPCION":empresa[4], "TIPO_EMPRESA":empresa[5], "CORREO":empresa[6], "TELEFONO":empresa[7], "NIT":empresa[8]}
            lista_empresas.append(new_empresa)
        return lista_empresas
    
    #Controlador para ver todos los repartidores en estado ACEPTADO para poder deshabilitarlo
def VerRepartidoresAdmin():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT R.REP_ID, R.NOMBRE, R.APELLIDO, R.USUARIO, R.CONTRASENA, R.CORREO, R.TELEFONO, R.NIT, R.LICENCIA, R.TRANSPORTE FROM REPARTIDOR R
        WHERE R.ESTADO = 'ACEPTADO';""")
        lista_repartidores = []
        repartidores = cursor.fetchall()
        for repartidor in repartidores:
            new_repartidor = {"REP_ID":repartidor[0], "NOMBRE":repartidor[1], "APELLIDO":repartidor[2], "USUARIO":repartidor[3], "CONTRASENA":repartidor[4], "CORREO":repartidor[5], "TELEFONO":repartidor[6], "NIT":repartidor[7],"LICENCIA":repartidor[8],"TRANSPORTE":repartidor[9]}
            lista_repartidores.append(new_repartidor)
        return lista_repartidores
    
        #Controlador para ver todos los clientes en estado ACEPTADO para poder deshabilitarlo
def VerClientesAdmin():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT C.CLI_ID, C.NOMBRE, C.APELLIDO, C.USUARIO, C.CONTRASENA, C.CORREO, C.TELEFONO, C.NIT, C.TARJETA FROM CLIENTE C
        WHERE C.ESTADO = 'ACEPTADO';""")
        lista_clientes = []
        clientes = cursor.fetchall()
        for cliente in clientes:
            new_cliente = {"CLI_ID":cliente[0], "NOMBRE":cliente[1], "APELLIDO":cliente[2], "USUARIO":cliente[3], "CONTRASENA":cliente[4], "CORREO":cliente[5], "TELEFONO":cliente[6], "NIT":cliente[7],"TARJETA":cliente[8]}
            lista_clientes.append(new_cliente)
        return lista_clientes
    

        #Controlador para ver todos las solicitudes de los repartidores
def VerSolicitudesRepartidores():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT S.SOL_ID, R.REP_ID, R.NOMBRE, R.APELLIDO, R.CORREO, R.TELEFONO, S.DESCRIPCION, S.FECHA, S.TIPO_SOLICITUD FROM SOLICITUD S
        INNER JOIN REPARTIDOR R on S.REPARTIDOR_REP_ID = R.REP_ID
        WHERE S.ESTADO = 'PENDIENTE' AND S.REPARTIDOR_REP_ID IS NOT NULL;""")
        lista_solicitudes = []
        solicitudes = cursor.fetchall()
        for solicitud in solicitudes:
            new_solicitud = {"SOL_ID":solicitud[0],"REP_ID":solicitud[1], "NOMBRE":solicitud[2], "APELLIDO":solicitud[3], "CORREO":solicitud[4], "TELEFONO":solicitud[5], "DESCRIPCION":solicitud[6], "FECHA":solicitud[7], "TIPO_SOLICITUD":solicitud[8]}
            lista_solicitudes.append(new_solicitud)
        return lista_solicitudes
    
#Controlador para ver todos las solicitudes de las empresas
def VerSolicitudesEmpresas():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT S.SOL_ID, E.EMP_ID, E.NOMBRE, E.CORREO, E.TELEFONO, S.DESCRIPCION, S.FECHA, S.TIPO_SOLICITUD FROM SOLICITUD S
        INNER JOIN  EMPRESA E on S.EMPRESA_EMP_ID = E.EMP_ID
        WHERE S.ESTADO = 'PENDIENTE' AND EMPRESA_EMP_ID IS NOT NULL;""")
        lista_solicitudes = []
        solicitudes = cursor.fetchall()
        for solicitud in solicitudes:
            new_solicitud = {"SOL_ID":solicitud[0], "EMP_ID":solicitud[1], "NOMBRE":solicitud[2], "CORREO":solicitud[3], "TELEFONO":solicitud[4], "DESCRIPCION":solicitud[5], "FECHA":solicitud[6], "TIPO_SOLICITUD":solicitud[7]}
            lista_solicitudes.append(new_solicitud)
        return lista_solicitudes
    
#Controlador para obtener la cantidad de pedidos en proceso que tiene la empresa
def VerPedidosProcesoEmpresa(id_emp):
    conexion = obtener_conexion()
    new_val = -1
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT COUNT(O.ESTADO) AS CANTIDAD FROM ORDEN O
        INNER JOIN DETALLE_ORDEN D on O.ORD_ID = D.ORDEN_ORD_ID
        INNER JOIN PRODUCTO P on D.PRODUCTO_PRO_ID = P.PRO_ID
        INNER JOIN EMPRESA E on P.EMPRESA_EMP_ID = E.EMP_ID
        WHERE E.EMP_ID = %s AND O.ESTADO = 'EN PROCESO';""",(id_emp,))
        valor = cursor.fetchone()[0]
        new_val = valor
    return new_val

#Controlador para obtener la cantidad de pedidos en proceso que tiene el repartidor
def VerPedidosProcesoRepartidor(id_rep):
    conexion = obtener_conexion()
    new_val = -1
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT COUNT(O.ESTADO) AS CANTIDAD FROM ORDEN O WHERE O.ESTADO = 'EN PROCESO' AND O.REPARTIDOR_REP_ID =%s;""",(id_rep,))
        valor = cursor.fetchone()[0]
        new_val = valor
    return new_val

#Controlador para obtener la cantidad de pedidos en proceso que tiene el cliente
def VerPedidosProcesoCliente(id_cli):
    conexion = obtener_conexion()
    new_val = -1
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT COUNT(O.ESTADO) AS CANTIDAD FROM ORDEN O WHERE O.ESTADO = 'EN PROCESO' AND O.CLIENTE_CLI_ID =%s;""",(id_cli,))
        valor = cursor.fetchone()[0]
        new_val = valor
    return new_val

#Controlador para crear la inhabilitacion de la empresa
def CrearInhabilitacionEmpresa(id_emp, id_rep, id_cli, tipo, fecha, descripcion):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""INSERT INTO INHABILITACION(EMPRESA_EMP_ID, REPARTIDOR_REP_ID, CLIENTE_CLI_ID, TIPO_INHABILITACION, FECHA, DESCRIPCION) VALUES(%s, %s, %s, %s, %s, %s)""",(id_emp, id_rep, id_cli, tipo, fecha, descripcion))
        conexion.commit()
        conexion.close()

#Controlador para crear la inhabilitacion del repartidor
def CrearInhabilitacionRepartidor(id_emp, id_rep, id_cli, tipo, fecha, descripcion):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""INSERT INTO INHABILITACION(EMPRESA_EMP_ID, REPARTIDOR_REP_ID, CLIENTE_CLI_ID, TIPO_INHABILITACION, FECHA, DESCRIPCION) VALUES(%s, %s, %s, %s, %s, %s)""",(id_emp, id_rep, id_cli, tipo, fecha, descripcion))
        conexion.commit()
        conexion.close()

#Controlador para crear la inhabilitacion del cliente
def CrearInhabilitacionCliente(id_emp, id_rep, id_cli, tipo, fecha, descripcion):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""INSERT INTO INHABILITACION(EMPRESA_EMP_ID, REPARTIDOR_REP_ID, CLIENTE_CLI_ID, TIPO_INHABILITACION, FECHA, DESCRIPCION) VALUES(%s, %s, %s, %s, %s, %s)""",(id_emp, id_rep, id_cli, tipo, fecha, descripcion))
        conexion.commit()
        conexion.close()

#Controlador para llamar al procedimiento de aceptar solicitudes como administrador
def AceptarSolicitudes(id_sol):
    conexion = obtener_conexion()
    salida = ""
    with conexion.cursor() as cursor:
        res = cursor.callproc("AceptarSolicitud", (id_sol, salida))
        conexion.commit()
        conexion.close()
        return res[1]
    

#Controlador para llamar al procedimiento de rechazar solicitudes como administrador
def RechazarSolicitudes(id_sol):
    conexion = obtener_conexion()
    salida = ""
    with conexion.cursor() as cursor:
        res = cursor.callproc("RechazarSolicitud", (id_sol, salida))
        conexion.commit()
        conexion.close()
        return res[1]
    
#Controlador para obtener el total de los detalles de una orden
def ObtenerTotalOrden(id_orden):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(""" SELECT IFNULL(combotot.TOTAL, 0)  + IFNULL(prodtot.TOTAL, 0)  as total FROM (
    (SELECT SUM(D.CANTIDAD * P.PRECIO) AS TOTAL FROM DETALLE_ORDEN D 
            INNER JOIN COMBO P on D.COMBO_COM_ID = P.COM_ID
            WHERE D.ORDEN_ORD_ID = %s)  AS combotot,
    (SELECT SUM(D.CANTIDAD * P.PRECIO) AS TOTAL FROM DETALLE_ORDEN D 
            INNER JOIN PRODUCTO P on D.PRODUCTO_PRO_ID = P.PRO_ID
            WHERE D.ORDEN_ORD_ID = %s)  as prodtot);""",(id_orden,id_orden,))
            total = cursor.fetchone()
            return total[0]
    except OperationalError as error:
        conexion.close()
        raise error
    finally:
        conexion.close()

#Controlador para insertar en la tabla VENTA la orden completada
def InsertarVenta(id_orden, total):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            print(f"id_orden: {id_orden} total:{total}")
            cursor.execute("""INSERT INTO VENTA(ORDEN_ORD_ID,FECHA, TOTAL) VALUES( %s, NOW(), %s)""",( id_orden,int(total)))
            conexion.commit()
            print('ok')
    except OperationalError as error:
        print(f"Error al insertar en la tabla VENTA: {error}")
        conexion.close()
        raise error
    finally:
        print('cerrando conexion')
        conexion.close()

#controlador para obtener el numero total de pedidos generados en el mes
def ObtenerPedidosMes():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT COUNT(ORD_ID) AS PEDIDOS FROM ORDEN WHERE MONTH(FECHA) = MONTH(NOW())""")
        total = cursor.fetchone()[0]
        return total

#controlador para obtener el total de los pedidos por empresa en el mes
def ObtenerTotalPedidosMesEmpresa(id_emp):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(""" SELECT TOTPRO.TOTAL + TOTCOMBO.TOTAL AS TOTAL FROM (
(SELECT SUM(PRODUCTO.PRECIO * DETALLE_ORDEN.CANTIDAD) AS TOTAL 
FROM ((ORDEN inner join DETALLE_ORDEN ON DETALLE_ORDEN.ORDEN_ORD_ID = ORDEN.ORD_ID)
inner join PRODUCTO ON PRODUCTO.PRO_ID = DETALLE_ORDEN.PRODUCTO_PRO_ID)
WHERE MONTH(ORDEN.FECHA) = MONTH(NOW()) AND PRODUCTO.EMPRESA_EMP_ID = %s) AS TOTPRO,
(SELECT SUM(COMBO.PRECIO * DETALLE_ORDEN.CANTIDAD) AS TOTAL 
FROM ((((ORDEN inner join DETALLE_ORDEN ON DETALLE_ORDEN.ORDEN_ORD_ID = ORDEN.ORD_ID)
inner join COMBO ON COMBO.COM_ID= DETALLE_ORDEN.COMBO_COM_ID)
INNER JOIN DETALLE_COMBO ON DETALLE_COMBO.COMBO_COM_ID = COMBO.COM_ID)
INNER JOIN PRODUCTO ON PRODUCTO.PRO_ID = DETALLE_COMBO.PRODUCTO_PRO_ID)
WHERE MONTH(ORDEN.FECHA) = MONTH(NOW()) AND PRODUCTO.EMPRESA_EMP_ID = %s) AS TOTCOMBO);""",(id_emp,id_emp,))
        total = cursor.fetchone()[0]
        return total

#obtener el conteo de pedidos por empresa en el mes
def ObtenerConteoPedidosMesEmpresa(id_emp):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT distinct COUNT(COMBO.COM_ID)
FROM (((((ORDEN inner join DETALLE_ORDEN ON DETALLE_ORDEN.ORDEN_ORD_ID = ORDEN.ORD_ID)
inner join COMBO ON COMBO.COM_ID= DETALLE_ORDEN.COMBO_COM_ID)
INNER JOIN PRODUCTO AS P ON P.PRO_ID = DETALLE_ORDEN.PRODUCTO_PRO_ID)
INNER JOIN DETALLE_COMBO ON DETALLE_COMBO.COMBO_COM_ID = COMBO.COM_ID)
INNER JOIN PRODUCTO AS PRP ON PRP.PRO_ID = DETALLE_COMBO.PRODUCTO_PRO_ID)
WHERE MONTH(ORDEN.FECHA) = MONTH(NOW()) AND (P.EMPRESA_EMP_ID = %s OR PRP.EMPRESA_EMP_ID = %s);""",(id_emp,id_emp,))
        total = cursor.fetchone()[0]
        return total 

#Controlador para obtener el total de las ventas generadas
def ObtenerVentasMes():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT SUM(TOTAL) AS TOTAL FROM VENTA WHERE MONTH(FECHA) = MONTH(NOW())""")
        total = cursor.fetchone()[0]
        return total

#obtener los productos mas vendidos
def ObtenerProductosMasVendidos():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT P.PRO_ID, P.NOMBRE, SUM(D.CANTIDAD) AS CANTIDAD 
        FROM PRODUCTO P INNER JOIN DETALLE_ORDEN D ON P.PRO_ID = D.PRODUCTO_PRO_ID 
        INNER JOIN ORDEN ON ORDEN.ORD_ID = D.ORDEN_ORD_ID
        WHERE MONTH(ORDEN.FECHA) = MONTH(now())
        GROUP BY P.PRO_ID ORDER BY CANTIDAD DESC LIMIT 5; """)
        productos = cursor.fetchall()
        return productos
    
#obtener los restaurantes que mas pedidos tienen
def ObtenerRestaurantesMasPedidos():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT E.EMP_ID, E.NOMBRE, COUNT(O.ORD_ID) AS CANTIDAD 
        FROM EMPRESA E INNER JOIN PRODUCTO P ON E.EMP_ID = P.EMPRESA_EMP_ID 
        INNER JOIN DETALLE_ORDEN D ON P.PRO_ID = D.PRODUCTO_PRO_ID 
        INNER JOIN ORDEN O ON D.ORDEN_ORD_ID = O.ORD_ID 
        WHERE E.TIPO_EMPRESA_T_EMP_ID = 1 AND month(O.FECHA) = month(now())
        GROUP BY E.EMP_ID ORDER BY CANTIDAD DESC LIMIT 5;""")
        restaurantes = cursor.fetchall()
        return restaurantes
    
#controlador para obtener la cantidad de clientes registrados
def ObtenerClientesRegistrados():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT COUNT(CLI_ID) AS CANTIDAD FROM CLIENTE WHERE ESTADO = 'ACEPTADO'""")
        cantidad = cursor.fetchone()[0]
        return cantidad
    
#Obtener los clientes que han realizado compras el ultimo mes
def ObtenerClientesComprasMes():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT CLI_ID, C.NOMBRE, C.APELLIDO, C.DIRECCION_DIR_ID ,C.CORREO, C.TELEFONO, C.NIT FROM CLIENTE C 
        INNER JOIN ORDEN O ON C.CLI_ID = O.CLIENTE_CLI_ID
        WHERE MONTH(O.FECHA) = MONTH(NOW());""")
        cantidadES = cursor.fetchall()
        return [{"id":cantidad[0], "nombre":cantidad[1], "apellido":cantidad[2], "direccion":cantidad[3], "correo":cantidad[4], "telefono":cantidad[5], "nit":cantidad[6]}for cantidad in cantidadES]
    
#obtener las empresas que fueron aprobadas por el administrador el ultimo mes
def ObtenerEmpresasAprobadasMes():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT EMP_ID, NOMBRE, EMPRESA.DIRECCION_DIR_ID, CORREO, TELEFONO 
FROM EMPRESA INNER JOIN SOLICITUD ON SOLICITUD.EMPRESA_EMP_ID = EMPRESA.EMP_ID
WHERE SOLICITUD.ESTADO = 'ACEPTADO' AND MONTH(FECHA) = MONTH(NOW());""")
        cantidadES = cursor.fetchall()
        return [{"id":cantidad[0], "nombre":cantidad[1], "direccion":cantidad[2], "correo":cantidad[3], "telefono":cantidad[4]}for cantidad in cantidadES]

#obtener los repartidores que fueron aprobados por el administrador el ultimo mes
def ObtenerRepartidoresAprobadosMes():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT REPARTIDOR.REP_ID, NOMBRE, APELLIDO, REPARTIDOR.DIRECCION_DIR_ID, CORREO, TELEFONO
FROM REPARTIDOR INNER JOIN SOLICITUD ON SOLICITUD.REPARTIDOR_REP_ID = REPARTIDOR.REP_ID
WHERE SOLICITUD.ESTADO = 'ACEPTADO' AND MONTH(FECHA) = MONTH(NOW());""")
        cantidadES = cursor.fetchall()
        return [{"id":cantidad[0], "nombre":cantidad[1], "apellido":cantidad[2], "direccion":cantidad[3], "correo":cantidad[4], "telefono":cantidad[5]}for cantidad in cantidadES]

#obtener los clientes que mas compras realizan
def ObtenerClientesMasCompras():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT C.CLI_ID, C.NOMBRE, C.APELLIDO, C.DIRECCION_DIR_ID ,C.CORREO, C.TELEFONO, C.NIT, COUNT(O.ORD_ID) AS CANTIDAD 
        FROM CLIENTE C INNER JOIN ORDEN O ON C.CLI_ID = O.CLIENTE_CLI_ID
     
        GROUP BY C.CLI_ID ORDER BY CANTIDAD DESC LIMIT 5;""")
        cantidadES = cursor.fetchall()
        return [{"id":cantidad[0], "nombre":cantidad[1], "apellido":cantidad[2], "direccion":cantidad[3], "correo":cantidad[4], "telefono":cantidad[5], "nit":cantidad[6], "cantidad":cantidad[7]}for cantidad in cantidadES]
    
#obtener el numero total de pedidos entregados en el mes
def ObtenerPedidosEntregadosMes():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT COUNT(ORD_ID) AS CANTIDAD FROM ORDEN WHERE ESTADO = 'ENTREGADO' AND MONTH(FECHA) = MONTH(NOW());""")
        cantidad = cursor.fetchone()[0]
        return cantidad
    
#obtener el promedio de tiempo que le toma a un repartidor entregar un pedido por mes
def ObtenerPromedioTiempoEntrega():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""select AVG(TIMESTAMPDIFF(HOUR, O.FECHA, VENTA.FECHA)) AS PROMEDIO_HORAS_REPARTIDOR 
FROM VENTA inner join ORDEN as O ON O.ORD_ID = VENTA.ORDEN_ORD_ID 
WHERE MONTH(O.FECHA) = MONTH(NOW()) AND O.ESTADO = 'ENTREGADO';""")
        cantidad = cursor.fetchone()[0]
        return cantidad
    
#obtener la calificacion promedio que tiene cada repartidor por mes
def ObtenerCalificacionPromedioRepartidor():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT REPARTIDOR.REP_ID, NOMBRE, APELLIDO, REPARTIDOR.DIRECCION_DIR_ID, CORREO, TELEFONO, AVG(CALIFICACION) AS CALIFICACION
FROM REPARTIDOR INNER JOIN ORDEN ON REPARTIDOR.REP_ID = ORDEN.REPARTIDOR_REP_ID
INNER JOIN VENTA ON ORDEN.ORD_ID = VENTA.ORDEN_ORD_ID
WHERE MONTH(ORDEN.FECHA) = MONTH(NOW()) AND ORDEN.ESTADO = 'ENTREGADO'
GROUP BY REPARTIDOR.REP_ID;""")
        cantidadES = cursor.fetchall()
        return [{"id":cantidad[0], "nombre":cantidad[1], "apellido":cantidad[2], "direccion":cantidad[3], "correo":cantidad[4], "telefono":cantidad[5], "calificacion":cantidad[6]}for cantidad in cantidadES]

    
#obtener las ganancias de cada repartidor en un mes
def ObtenerGananciasRepartidorMes():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT REPARTIDOR.REP_ID, NOMBRE, APELLIDO, REPARTIDOR.DIRECCION_DIR_ID, CORREO, TELEFONO, SUM(VENTA.TOTAL) AS GANANCIA
FROM REPARTIDOR INNER JOIN ORDEN ON REPARTIDOR.REP_ID = ORDEN.REPARTIDOR_REP_ID
INNER JOIN VENTA ON ORDEN.ORD_ID = VENTA.ORDEN_ORD_ID
WHERE MONTH(ORDEN.FECHA) = MONTH(NOW()) AND ORDEN.ESTADO = 'ENTREGADO'
GROUP BY REPARTIDOR.REP_ID;""")
        cantidadES = cursor.fetchall()
        return [{"id":cantidad[0], "nombre":cantidad[1], "apellido":cantidad[2], "direccion":cantidad[3], "correo":cantidad[4], "telefono":cantidad[5], "ganancia":cantidad[6]}for cantidad in cantidadES]

# Controlador para ver los pedidos realizados a una empresa y su total de ventas
def ObtenerNoPedidosYTotalVentas(id_empresa):
    conexion = obtener_conexion()
    registros = []
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT COUNT(ORD_ID) AS CANTIDAD_ORDENES, SUM(VENTA) AS VENTA_TOTAL 
                        FROM (SELECT o.ORD_ID,
                        SUM(if(do.COMBO_COM_ID IS NULL, do.CANTIDAD, do.CANTIDAD * dc.CANTIDAD) * if(do.COMBO_COM_ID IS NULL, p.PRECIO, c.PRECIO)) AS VENTA
                        FROM ORDEN o 
                        INNER JOIN DETALLE_ORDEN do ON do.ORDEN_ORD_ID = o.ORD_ID 
                        LEFT JOIN PRODUCTO p ON p.PRO_ID = do.PRODUCTO_PRO_ID
                        LEFT JOIN COMBO c ON c.COM_ID = do.COMBO_COM_ID
                        LEFT JOIN DETALLE_COMBO dc ON dc.COMBO_COM_ID = c.COM_ID 
                        LEFT JOIN PRODUCTO p2 ON p2.PRO_ID = dc.PRODUCTO_PRO_ID 
                        WHERE (p.EMPRESA_EMP_ID = %s OR p2.EMPRESA_EMP_ID = %s) AND o.ESTADO = 'RECIBIDO'
                        GROUP BY ORD_ID) AS query_final """, (id_empresa, id_empresa, ))
        registros = cursor.fetchall()
        registros = [{"CANTIDAD_ORDENES":registro[0], "CANTIDAD_VENTA":registro[1]}for registro in registros]
    conexion.close()
    return registros

# Controlador para obtener el top 5 productos mas vendidos
def Top5ProductosMasVendidos(id_empresa):
    conexion = obtener_conexion()
    registros = []
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT PROD_ID, NOMBRE, SUM(CANTIDAD_VENDIDOS) AS CANTIDAD_VENDIDOS
        FROM (SELECT if(do.COMBO_COM_ID IS NULL, p.PRO_ID, p2.PRO_ID) AS PROD_ID, 
        if(do.COMBO_COM_ID IS NULL, p.NOMBRE, p2.NOMBRE) AS NOMBRE, 
        SUM(do.CANTIDAD * if(do.COMBO_COM_ID IS NULL, 1, dc.CANTIDAD)) AS CANTIDAD_VENDIDOS
        FROM ORDEN o
        INNER JOIN DETALLE_ORDEN do ON do.ORDEN_ORD_ID = o.ORD_ID 
        LEFT JOIN PRODUCTO p ON p.PRO_ID = do.PRODUCTO_PRO_ID
        LEFT JOIN COMBO c ON c.COM_ID = do.COMBO_COM_ID
        LEFT JOIN DETALLE_COMBO dc ON dc.COMBO_COM_ID = c.COM_ID 
        LEFT JOIN PRODUCTO p2 ON p2.PRO_ID = dc.PRODUCTO_PRO_ID
        WHERE (p.EMPRESA_EMP_ID = %s OR p2.EMPRESA_EMP_ID = %s) AND o.ESTADO = 'RECIBIDO'
        GROUP BY p.PRO_ID, p2.PRO_ID) AS query_final
        GROUP BY PROD_ID
        ORDER BY CANTIDAD_VENDIDOS DESC
        Limit 5 """, (id_empresa, id_empresa, ))
        registros = cursor.fetchall()
        registros = [{"PROD_ID":registro[0], "NOMBRE":registro[1], "CANTIDAD_VENDIDOS":registro[2]}for registro in registros]
    conexion.close()
    return registros



def VentasXD():
    print("hola")
    conexion = obtener_conexion()
    cantidades = None
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT ORDEN.ORD_ID,EMPRESA.NOMBRE AS EMPRESA, SUM(PRODUCTO.PRECIO * DETALLE_ORDEN.CANTIDAD) AS TOTAL
                        FROM ORDEN
                        JOIN CLIENTE ON ORDEN.CLIENTE_CLI_ID = CLIENTE.CLI_ID
                        JOIN DETALLE_ORDEN ON ORDEN.ORD_ID = DETALLE_ORDEN.ORDEN_ORD_ID
                        JOIN PRODUCTO ON DETALLE_ORDEN.PRODUCTO_PRO_ID = PRODUCTO.PRO_ID
                        JOIN EMPRESA ON PRODUCTO.EMPRESA_EMP_ID = EMPRESA.EMP_ID
                        GROUP BY EMPRESA.NOMBRE;""")
        cantidades= cursor.fetchall()
        conexion.close()
        return [{"id":str(cantidad[0]), "empresa":str(cantidad[1]), "total":str(cantidad[2])}for cantidad in cantidades]

    

def ObtenerVentas():

    conexion = obtener_conexion()
    cantidades = None
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT ORDEN_ORD_ID, SUM(PRECIO * CANTIDAD) AS VALOR_VENTA
                        FROM DETALLE_ORDEN
                        INNER JOIN PRODUCTO ON DETALLE_ORDEN.PRODUCTO_PRO_ID = PRODUCTO.PRO_ID
                        GROUP BY ORDEN_ORD_ID;""")
        cantidades= cursor.fetchall()
        conexion.close()
        return [{"id":str(cantidad[0]), "total":str(cantidad[1])}for cantidad in cantidades]


def ProductosMasVendidos():

    conexion = obtener_conexion()
    cantidades = None
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT 
                            p.PRO_ID,
                            p.NOMBRE,
                            SUM(d.CANTIDAD) AS TOTAL_VENDIDO
                            FROM
                            PRODUCTO p
                            INNER JOIN DETALLE_ORDEN d ON p.PRO_ID = d.PRODUCTO_PRO_ID
                            GROUP BY
                            p.PRO_ID
                            ORDER BY
                            TOTAL_VENDIDO DESC;""")
        cantidades= cursor.fetchall()
        conexion.close()
        return [{"id":str(cantidad[0]), "nombre":str(cantidad[1]), "total":str(cantidad[2])}for cantidad in cantidades]



def TotalClientes():
    conexion = obtener_conexion()
    cantidades = None
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT COUNT(*) AS total_clientes FROM CLIENTE;""")
        cantidades= cursor.fetchall()
        conexion.close()
        return [{"total":str(cantidad[0])}for cantidad in cantidades]


 
def ClientesActivos():
    conexion = obtener_conexion()
    cantidades = None
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT COUNT(*) AS total_clientes FROM CLIENTE WHERE LOWER(ESTADO) = 'activo';""")
        cantidades= cursor.fetchall()
        conexion.close()
        return [{"total":str(cantidad[0])}for cantidad in cantidades]


def PedidosRepartidor():
    conexion = obtener_conexion()
    cantidades = None
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT COUNT(*) AS num_pedidos, REPARTIDOR_REP_ID, CONCAT(R.NOMBRE, " ",R.APELLIDO) AS NOMBRE
                        FROM ORDEN
                        INNER JOIN REPARTIDOR R ON R.REP_ID = ORDEN.REPARTIDOR_REP_ID 
                        WHERE REPARTIDOR_REP_ID IS NOT NULL;""")
        cantidades= cursor.fetchall()
        conexion.close()
        return [{"id":str(cantidad[1]), "nombre":str(cantidad[2]), "total":str(cantidad[0])}for cantidad in cantidades]



def PromedioCalificacion():
    conexion = obtener_conexion()
    cantidades = None
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT REP_ID, AVG(CALIFICACION) AS PROMEDIO_CALIFICACION, CONCAT(REPARTIDOR.NOMBRE, " ",REPARTIDOR.APELLIDO) AS NOMBRE
                        FROM REPARTIDOR
                        LEFT JOIN ORDEN ON REPARTIDOR.REP_ID = ORDEN.REPARTIDOR_REP_ID
                        GROUP BY REP_ID;""")
        cantidades= cursor.fetchall()
        conexion.close()
        return [{"id":str(cantidad[0]), "nombre":str(cantidad[2]), "promedio":str(cantidad[1])}for cantidad in cantidades]