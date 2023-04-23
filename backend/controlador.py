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
        cursor.execute("""SELECT o.ORD_ID, c.CLI_ID, CONCAT(c.NOMBRE, ', ', c.APELLIDO) AS NOMBRE_COMPLETO_CLIENTE, d.LUGAR, 
        r.REP_ID, CONCAT(r.NOMBRE, ', ', r.APELLIDO) AS NOMBRE_COMPLETO_REPARTIDOR, DATE_FORMAT(o.FECHA, '%d/%m/%Y') AS FECHA, o.ESTADO, o.CALIFICACION,
        JSON_ARRAYAGG(JSON_OBJECT(
        'ID_ARTICULO', CASE WHEN c2.COM_ID IS NULL THEN p.PRO_ID ELSE c2.COM_ID END, 
        'NOMBRE_ARTICULO', CASE WHEN c2.NOMBRE IS NULL THEN p.NOMBRE ELSE c2.NOMBRE END, 
        'PRECIO_ARTICULO', CASE WHEN c2.PRECIO IS NULL THEN p.PRECIO ELSE c2.PRECIO END,
        'ES_COMBO', CASE WHEN c2.COM_ID IS NULL THEN FALSE ELSE TRUE END
        ))
        FROM ORDEN o
        INNER JOIN CLIENTE c ON c.CLI_ID = o.CLIENTE_CLI_ID 
        INNER JOIN DIRECCION d ON d.DIR_ID = o.DIRECCION_DIR_ID 
        INNER JOIN REPARTIDOR r ON r.REP_ID = o.REPARTIDOR_REP_ID 
        INNER JOIN DETALLE_ORDEN do ON do.ORDEN_ORD_ID = o.ORD_ID
        LEFT JOIN COMBO c2 ON c2.COM_ID = do.COMBO_COM_ID 
        LEFT JOIN PRODUCTO p ON p.PRO_ID = do.PRODUCTO_PRO_ID  
        WHERE (p.EMPRESA_EMP_ID = %s OR c2.COM_ID IN (SELECT COMBO_COM_ID FROM DETALLE_COMBO dc 
        INNER JOIN PRODUCTO p ON p.PRO_ID = dc.PRODUCTO_PRO_ID
        WHERE p.EMPRESA_EMP_ID = %s)) AND o.ESTADO = 'PENDIENTE'
        GROUP BY o.ORD_ID""", (id_empresa, id_empresa ))
        combos = cursor.fetchall()
        
        if combos:
            combos = [{"ORD_ID":combo[0], "CLI_ID":combo[1], "NOMBRE_COMPLETO_CLIENTE":combo[2], "LUGAR":combo[3], "REP_ID":combo[4], "NOMBRE_COMPLETO_REPARTIDOR": combo[5], "FECHA": combo[6], "ESTADO": combo[7], "CALIFICACION": combo[8], "DETALLE_ORDEN":json.loads(combo[9])}for combo in combos]
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
        cursor.execute("SELECT * FROM REPARTIDOR WHERE USUARIO = %s and CONTRASENA = %s", (usuario,contraseña,))
        usuariosend = cursor.fetchone()
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
                          "VALUES (" + str(id_combo) + "," + str(id_orden) + "," + str(id_producto) + "," + str(cantidad) + ",'" + observaciones + "','" + "pendiente" + "');")
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
        "VALUES (" + str(id_cliente) + "," + str(id_direccion) + ",NULL , NOW(),'" + "pendiente" + "','" + str(calificacion) + "','" + comentario + "','" + metodo_pago + "');")
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
def VerPedidosPendientesRepartidor():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT ORD_ID, C.NOMBRE, C.APELLIDO, D2.NOMBRE, M.NOMBRE, D.LUGAR, O.METODO_PAGO, O.ESTADO  FROM ORDEN O
        INNER JOIN CLIENTE C on O.CLIENTE_CLI_ID = C.CLI_ID
        INNER JOIN DIRECCION D on O.DIRECCION_DIR_ID = D.DIR_ID
        INNER JOIN MUNICIPIO M on D.MUNICIPIO_MUN_ID = M.MUN_ID
        INNER JOIN DEPARTAMENTO D2 on M.DEPARTAMENTO_DEP_ID = D2.DEP_ID
        INNER JOIN REPARTIDOR R on O.REPARTIDOR_REP_ID = R.REP_ID
        INNER JOIN DIRECCION D3 on R.DIRECCION_DIR_ID = D3.DIR_ID
        INNER JOIN MUNICIPIO M2 on D3.MUNICIPIO_MUN_ID = M2.MUN_ID
        WHERE O.ESTADO = 'RECIBIDO' AND O.REPARTIDOR_REP_ID = NULL AND D2.DEP_ID = M2.DEPARTAMENTO_DEP_ID;""")
        pendientes = cursor.fetchall()
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
        cursor.execute("SELECT ORD_ID FROM ORDEN WHERE ESTADO = 'EN PROCESO' AND REPARTIDOR_REP_ID =" + str(rep_id))
        id_ord = cursor.fetchone()[0]
        conexion.close()
        return id_ord 

#Controlador para retornar la orden asignada al repartidor
def VerPedidoAsignadoRepartidor(nombre):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        id_usuario = VerIdRepartidorLog(nombre)
        id_ord = VerIdOrdenAsignadaRepartidor(id_usuario)
        cursor.execute("""SELECT O.ORD_ID, C.NOMBRE, C.APELLIDO, D2.NOMBRE, M.NOMBRE, D.LUGAR, O.METODO_PAGO, O.ESTADO FROM ORDEN O
        INNER JOIN CLIENTE C on O.CLIENTE_CLI_ID = C.CLI_ID
        INNER JOIN DIRECCION D on O.DIRECCION_DIR_ID = D.DIR_ID
        INNER JOIN MUNICIPIO M on D.MUNICIPIO_MUN_ID = M.MUN_ID
        INNER JOIN DEPARTAMENTO D2 on M.DEPARTAMENTO_DEP_ID = D2.DEP_ID
        WHERE O.ESTADO = 'EN PROCESO' AND O.ORD_ID = %s""", (id_ord,))
        pedido = cursor.fetchone()[0]
        cursor.execute("""SELECT C.NOMBRE, P.NOMBRE, D.CANTIDAD  FROM DETALLE_ORDEN D
        INNER JOIN COMBO C on D.COMBO_COM_ID = C.COM_ID
        INNER JOIN PRODUCTO P on D.PRODUCTO_PRO_ID = P.PRO_ID
        WHERE D.ORDEN_ORD_ID = %s""",(id_ord,))
        lista_p = []
        new_prod = None
        lista_productos = cursor.fetchall()
        for producto in lista_productos:
            if producto[0] != None:
                new_prod = {"PROMOCION":producto[0], "CANTIDAD":producto[2]}
                lista_p.append(new_prod)
            elif producto[1] != None:
                new_prod = {"PRODUCTO":producto[1], "CANTIDAD":producto[2]}
                lista_p.append(new_prod)
        asignado = {"ORD_ID":pedido[0],"CLIENTE":pedido[1]+" "+pedido[2], "DEPARTAMENTO":pedido[3], "MUNICIPIO":pedido[4], "LUGAR":pedido[5], "METODO_PAGO":pedido[6], "ESTADO":pedido[7], "PRODUCTOS":lista_p}
        return asignado
    
#Controlador para cambiar el estado del producto asignado
def AsignarPedidoRepartidor(id_ord, usuario_rep):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("CALL AsignarPedidoRepartidor(%s,%s)", (id_ord, usuario_rep))
        conexion.commit()
        conexion.close()

#Controlador para cambiar el estado del pedido a "entregado" 
def EntregarPedidoRepartidor(ord_id, usuario):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""UPDATE ORDEN O
        INNER JOIN REPARTIDOR R on O.REPARTIDOR_REP_ID = R.REP_ID
        SET O.ESTADO = 'ENTREGADO'
        WHERE O.ESTADO = 'EN PROCESO' AND O.ORD_ID=%s AND R.USUARIO = %s;""", (ord_id, usuario))
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
        cursor.execute("""SELECT R.NOMBRE, R.APELLIDO, R.USUARIO, R.CONTRASENA, R.CORREO, R.NIT, D2.NOMBRE, M.NOMBRE, D.LUGAR, R.LICENCIA, R.TRANSPORTE, R.DOCUMENTO FROM REPARTIDOR R
        INNER JOIN DIRECCION D on R.DIRECCION_DIR_ID = D.DIR_ID
        INNER JOIN MUNICIPIO M on D.MUNICIPIO_MUN_ID = M.MUN_ID
        INNER JOIN DEPARTAMENTO D2 on M.DEPARTAMENTO_DEP_ID = D2.DEP_ID
        WHERE R.USUARIO =%s """,(usuario,))
        logueado = cursor.fetchone()[0]
        calificacion = VerCalificacionPromedioRepartidor(usuario, mes)
        comision = VerComisionRepartidor(usuario, mes)
        new_user = {"NOMBRE":logueado[0], "APELLIDO":logueado[1], "USUARIO":logueado[2], "CONTRASENA":logueado[3], "CORREO":logueado[4], "NIT":logueado[5], "DEPARTAMENTO":logueado[6], "MUNICIPIO":logueado[7], "LUGAR":logueado[8], "LICENCIA":logueado[9], "TRANSPORTE":logueado[10],"DOCUMENTO":logueado[11],"CALIFICACION":calificacion, "COMISION":comision}
        conexion.close()
        return new_user
       
#Controlador que retorna la calificacion promedio en el mes del repartidor logueado
def VerCalificacionPromedioRepartidor(usuario, mes):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT AVG(O.CALIFICACION) FROM ORDEN O
        INNER JOIN REPARTIDOR R on O.REPARTIDOR_REP_ID = R.REP_ID
        WHERE R.USUARIO = %s AND MONTH(O.FECHA) = %s;""",(usuario,mes))
        valor = cursor.fetchone()[0]
        conexion.close()
        return valor
    
#Controlador para ver las comisiones generadas en el mes del repartidor logueado
def VerComisionRepartidor(usuario, mes):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT SUM(V.TOTAL)*0.05 AS COMISION FROM VENTA V
        INNER JOIN ORDEN O on V.ORDEN_ORD_ID = O.ORD_ID
        INNER JOIN REPARTIDOR R on O.REPARTIDOR_REP_ID = R.REP_ID
        WHERE R.USUARIO =%s AND MONTH(V.FECHA) = %s""", (usuario, mes)) 
        valor = cursor.fetchone()[0]
        conexion.close()
        return valor

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
def ActualizarPerfilRepartidor(correo,contrasena, nit, telefono, transporte, licencia, documento,usuario):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""UPDATE REPARTIDOR R
        INNER JOIN DIRECCION D on R.DIRECCION_DIR_ID = D.DIR_ID
        SET R.CORREO = %s,
        R.CONTRASENA = %s,
        R.NIT = %s,
        R.TELEFONO = %s,
        R.TRANSPORTE = %s,
        R.LICENCIA =%s,
        R.DOCUMENTO = %s
        WHERE R.USUARIO =%s;""",(correo,contrasena, nit, telefono, transporte, licencia, documento,usuario))
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