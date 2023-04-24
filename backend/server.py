from conexion import obtener_conexion
import controlador
from flask import Flask, jsonify, request, Response, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = '../public'
ALLOWED_EXTENSIONS = set(['png','svg','jpg','pdf'])

@app.route('/', methods=['GET'])
def index():
    try:
        conexion = obtener_conexion()
        print("CONEXION EXITOSA")
        return jsonify({'AYD1': "Proyecto, AYD1 CONEXION EXITOSA"})
    except:
        print("NO SE PUEDE ESTABLECER LA CONEXION A LA BASE DE DATOS")
        return jsonify({'AYD1': "NO SE PUEDE ESTABLECER LA CONEXION A LA BASE DE DATOS"})

# Endpoint para obtener un cliente existente en la base de datos
@app.route('/loguearCliente/<nombre>/<contrasenia>', methods=['GET'])
def LoguearCliente(nombre, contrasenia):
    usuario = controlador.LoguearCliente(nombre, contrasenia)
    return jsonify({"respuesta":usuario})

# Endpoint para obtener una empresa existente en la base de datos
@app.route('/loguearEmpresa/<nombre>/<contrasenia>', methods=['GET'])
def LoguearEmpresa(nombre, contrasenia):
    empresa = controlador.LoguearEmpresa(nombre, contrasenia)
    return jsonify({"respuesta":empresa})

# Endpoint para mostrar todos los departamentos registrados en la base de datos
@app.route('/mostrarDepartamentos', methods=["GET"])
def MostrarDepartamentos():
    try:
        departamentos = controlador.VerDepartamentos()
        return jsonify(departamentos)
    except Exception as e:
        return jsonify({'respuesta': "Error al obtener los departamentos" + e})

# Endpoint para mostrar todos los municipios registrados en la base de datos
@app.route('/mostrarMunicipios', methods=["GET"])
def MostrarMunicipio():
    try:
        municipios = controlador.VerMunicipios()
        return jsonify(municipios)
    except Exception as e:
        return jsonify({'respuesta': "Error al obtener los municipios" + e})

# Endpoint para mostrar todos los municipios registrados en la base de datos
# segun el parametro 'id_departamento'
@app.route('/mostrarMunicipios/<id_departamento>', methods=["GET"])
def MostrarMunicipioID(id_departamento):
    try:
        municipios = controlador.ObtenerMunicipios(id_departamento)
        return jsonify(municipios)
    except Exception as e:
        return jsonify({'respuesta': "Error al obtener los municipios" + e})

# Endpoint para mostrar todos los tipos de empresas registrados en la base de datos
@app.route('/mostrarTiposEmpresa', methods=["GET"])
def MostrarTipoEmpresa():
    try:
        tipos_empresa = controlador.VerTiposEmpresa()
        return jsonify(tipos_empresa)
    except Exception as e:
        return jsonify({'respuesta': "Error al obtener los tipos de empresa" + e})

# Endpoint para mostrar todos los productos que posee una empresa en la base de datos
@app.route('/mostrarProductosEmpresa/<id_empresa>', methods=["GET"])
def MostrarProductosEmpresa(id_empresa):
    try:
        productos_empresa = controlador.ObtenerProductosEmpresa(id_empresa)
        return jsonify(productos_empresa)
    except Exception as e:
        return jsonify({'respuesta': "Error al obtener los productos de la empresa: " + str(e)})

# Endpoint para mostrar todos los productos que posee una empresa y se utiliza el parametro
# id_tipo_producto para filtrarlos por tipo de producto
@app.route('/mostrarProductosEmpresa/<id_empresa>/<id_tipo_producto>', methods=["GET"])
def MostrarProductosEmpresaTipoProducto(id_empresa, id_tipo_producto):
    try:
        productos_empresa = controlador.ObtenerProductosEmpresaTipoProducto(id_empresa, id_tipo_producto)
        return jsonify(productos_empresa)
    except Exception as e:
        return jsonify({'respuesta': "Error al obtener los productos de la empresa: " + str(e)})

#Endpoint para mostrar todas las ordenes existentes con su respectivo detalle
@app.route('/mostrarOrdenes/<id_empresa>', methods=['GET'])
def MostrarOrdenes(id_empresa):
    try:
        respuesta = controlador.MostrarOrdenes(id_empresa)
        return jsonify({"exito":True, "msg":respuesta})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al mostrar la informacion: " + str(e)})

# Endpoint para almacenar una empresa en la base de datos
@app.route('/crearEmpresa', methods=['POST'])
def CrearEmpresa():
    try:
        # Verificando si ya existe el usuario en la base de datos
        id_usuario_empresa = controlador.ObtenerUsuarioEmpresa(request.form['usuario'])
        if id_usuario_empresa is not None:
            return jsonify({'exito':False, "msg": "El nombre de usuario que ha elegido no está disponible. Por favor, pruebe con otro nombre de usuario."})

        # Verificando si ya existe la direccion en la base de datos
        id_direccion = controlador.ObtenerDireccion(request.form['id_municipio'], request.form['lugar'])
        if id_direccion is None:
            id_direccion = controlador.AgregarDireccion(request.form['id_municipio'], request.form['lugar'])
        else:
            id_direccion = id_direccion[0]

        id_tipo_empresa = request.form['id_tipo_empresa']
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        correo = request.form['correo']
        telefono = request.form['telefono']
        usuario = request.form['usuario']
        contrasenia = request.form['contrasenia']
        nit = request.form['nit']

        nombre_archivo = None
        if('documento' in request.files):
            documento = request.files['documento']
            filename = secure_filename(documento.filename)
            if(not archivo_permitido(filename)):
                return jsonify({"exito":False, "msg":"La extensión del archivo no esta permitido"})

            hora_actual = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") # Obtiene la hora actual como una cadena en el formato "YYYY-MM-DD-HH-MM-SS"
            nombre_archivo = hora_actual + '_' + filename # Concatena la hora actual y el nombre de archivo original
            documento.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo))

        id_empresa = controlador.AgregarEmpresa(id_direccion, id_tipo_empresa, nombre, descripcion, correo, telefono, usuario, contrasenia, nit, nombre_archivo)
        controlador.AgregarSolicitud(id_empresa, None, "empresa", datetime.now().strftime("%Y-%m-%d-%H-%M-%S"), "Solicitud de creación de usuario de tipo empresa", "pendiente")
        return jsonify({"exito":True, "msg":"Se ha creado su usuario correctamente. Le pedimos que aguarde la confirmación de su cuenta"})
    except Exception as e:
        controlador.EliminarEmpresa(id_empresa)
        return jsonify({'exito':False, "msg": "Error al crear su usuario: " + str(e)})

#Endpoint para comprobar si la contrasenia y usuario admin son correctos
@app.route('/inicioSesionAdmin/<USER>/<CONTRA>', methods=['GET'])
def inicioSesionAdmin(USER, CONTRA):
    try:
        usuario=controlador.VerificarSesAdmin(USER, CONTRA)
        if  usuario != None:
            return jsonify({'exito':True, "respuesta":{'USUARIO': usuario[0]}})
        else:
            return jsonify({'exito':False, "msg": "Error credenciales incorrectas"})

    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al intentar iniciar sesion: " + str(e)})

#Endpoint para comprobar si la contrasenia y usuario admin son correctos
@app.route('/inicioSesionRepartidor/<USER>/<CONTRA>', methods=['GET'])
def inicioSesionRepartidor(USER, CONTRA):
    try:
        usuario=controlador.VerificarSesRepartidor(USER, CONTRA)
        if  usuario != None:
            return jsonify({'exito':True, "respuesta":{'USUARIO': usuario[0]}})
        else:
            return jsonify({'exito':False, "msg": "Error credenciales incorrectas"})

    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al intentar iniciar sesion: " + str(e)})


def archivo_permitido(name):
    name = name.split('.')
    if(name[-1] in ALLOWED_EXTENSIONS):
        return True
    return False

# Endpoint para almacenar un producto en la base de datos
@app.route('/crearProducto', methods=['POST'])
def CrearProducto():
    try:
        id_empresa = request.form['id_empresa']
        id_tipo_producto = request.form['id_tipo_producto']
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']

        nombre_archivo = None
        if('documento' in request.files):
            documento = request.files['documento']
            filename = secure_filename(documento.filename)
            if(not archivo_permitido(filename)):
                return jsonify({"exito":False, "msg":"La extensión del archivo no esta permitido"})

            hora_actual = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") # Obtiene la hora actual como una cadena en el formato "YYYY-MM-DD-HH-MM-SS"
            nombre_archivo = hora_actual + '_' + filename # Concatena la hora actual y el nombre de archivo original
            documento.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo))

        id_empresa = controlador.AgregarProducto(id_empresa, id_tipo_producto, nombre, descripcion, precio, stock, nombre_archivo)
        return jsonify({"exito":True, "msg":"Se ha creado su producto correctamente."})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al crear su producto: " + str(e)})

@app.route('/registrarRepartidor', methods=['POST'])
def registrarRepartidor():
    info = request.form
    nombre = info['nombre']
    apellido = info['apellido']
    telefono = info['telefono']
    correo = info['correo']
    usuario = info['usuario']
    contra = info['contra']
    nit = info['nit']
    lugar = info['lugar']
    licencia = info['licencia']
    transporte = info['transporte']
    id_muni = info['id_muni']
    id_dep = info['id_dep']
    existencia = controlador.ExistenciaUsuario(usuario, "REPARTIDOR")
    if existencia:
        return jsonify({
        "status": "failed",
        "message": "El usuario " + usuario + " ya existe, intente denuevo."
        })
    try:
        nombre_archivo = None
        if('documento' in request.files):
            documento = request.files['documento']
            filename = secure_filename(documento.filename)
            if(not archivo_permitido(filename)):
                return jsonify({
                    "status": "failed",
                    "message":"La extensión del archivo no esta permitido"
                    })
            hora_actual = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            nombre_archivo = hora_actual + '_' + filename 
            documento.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo))
        id_repartidor = controlador.RegistrarRepartidor(nombre, apellido, usuario, contra, correo, telefono, nit, id_dep, id_muni, lugar, licencia, transporte, nombre_archivo)
        id_empresa = controlador.UltimaEmpresa()
        controlador.AgregarSolicitud(id_empresa, id_repartidor, "repartidor", datetime.now().strftime("%Y-%m-%d-%H-%M-%S"), "Solicitud de creación de usuario de tipo repartidor", "pendiente")
        return jsonify({
        "status": "success",
        "message": "Se ha registrado su usuario correctamente, espere a que sea aprobado por un administrador."
        })
    except:
        return jsonify({
        "status": "failed",
        "message": "Ocurrio un error inesperado, intentelo denuevo."
        })

@app.route('/registrarCliente', methods=['POST'])
def registrarCliente():
    info = request.json
    nombre = info['nombre']
    apellido = info['apellido']
    telefono = info['telefono']
    correo = info['correo']
    usuario = info['usuario']
    contra = info['contra']
    nit = info['nit']
    lugar = info['lugar']
    id_muni = info['id_muni']
    id_dep = info['id_dep']
    tarjeta = info['tarjeta']

    existencia = controlador.ExistenciaUsuario(usuario, "CLIENTE")
    if existencia:
        return jsonify({
        "status": "failed",
        "message": "El usuario " + usuario + " ya existe, intente denuevo."
        })
    try:
        controlador.RegistrarCliente(nombre, apellido, usuario, contra, correo, telefono, nit, id_dep, id_muni, lugar, tarjeta)
        return jsonify({
        "status": "success",
        "message": "El cliente ha sido registrado exitosamente"
        })
    except:
        return jsonify({
        "status": "failed",
        "message": "Ocurrio un error inesperado, intentelo denuevo."
        })

# Endpoint para almacenar un combo en la base de datos
@app.route('/crearCombo', methods=['POST'])
def CrearCombo():
    try:
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        nombre_archivo = None
        if('documento' in request.files):
            documento = request.files['documento']
            filename = secure_filename(documento.filename)
            if(not archivo_permitido(filename)):
                return jsonify({"exito":False, "msg":"La extensión del archivo no esta permitido"})

            hora_actual = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") # Obtiene la hora actual como una cadena en el formato "YYYY-MM-DD-HH-MM-SS"
            nombre_archivo = hora_actual + '_' + filename # Concatena la hora actual y el nombre de archivo original
            documento.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo))

        controlador.CrearCombo(nombre, descripcion, precio, nombre_archivo)
        return jsonify({"exito":True, "msg":"Se ha creado su combo correctamente."})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al crear su combo: " + str(e)})

# Endpoint para almacenar un producto a un combo y asi ir formando el detalle del combo
@app.route('/agregarProductoACombo', methods=['POST'])
def AgregarProductoACombo():
    try:
        id_combo = request.form['id_combo']
        id_producto = request.form['id_producto']
        cantidad = request.form['cantidad']
        observaciones = request.form['observaciones']
        ids_productos = controlador.ObtenerProductoCombo(id_combo)
        if (int(id_producto), ) in ids_productos :
            return jsonify({"exito":False, "msg":"Este producto ya esta en el detalle del combo"})
        else:
            controlador.AgregarProductoACombo(id_combo, id_producto, cantidad, observaciones)
            return jsonify({"exito":True, "msg":"Se ha agregado el producto al combo correctamente."})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al agregar el producto al combo: " + str(e)})

# Endpoint para eliminar un producto en la base de datos
@app.route('/eliminarProducto/<id_producto>', methods=["DELETE"])
def EliminarProducto(id_producto):
    try:
        controlador.EliminarProducto(id_producto)
        return jsonify({"exito":True, "msg":"Se ha eliminado correctamente su producto."})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al eliminar su producto: " + str(e)})

# Endpoint para eliminar un producto en la base de datos
@app.route('/eliminarCombo/<id_combo>', methods=["DELETE"])
def EliminarCombo(id_combo):
    try:
        info_combo = controlador.ObtenerCombo(id_combo)
        if info_combo is not None:
            controlador.EliminarDetalleCombo(id_combo)
            controlador.EliminarCombo(id_combo)
            os.remove(app.config['UPLOAD_FOLDER'] + "/"+ info_combo[0]['FOTOGRAFIA'])
        return jsonify({"exito":True, "msg":"Se ha eliminado correctamente su combo."})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al eliminar su combo: " + str(e)})

# Endpoint para actualizar la informacion de un producto
@app.route('/actualizarProducto/<id_producto>', methods=["PUT"])
def ActualizarProducto(id_producto):
    try:
        id_tipo_producto = request.form['id_tipo_producto']
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']

        nombre_archivo = None
        if('documento' in request.files):
            documento = request.files['documento']
            filename = secure_filename(documento.filename)
            if(not archivo_permitido(filename)):
                return jsonify({"exito":False, "msg":"La extensión del archivo no esta permitido"})

            hora_actual = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") # Obtiene la hora actual como una cadena en el formato "YYYY-MM-DD-HH-MM-SS"
            nombre_archivo = hora_actual + '_' + filename # Concatena la hora actual y el nombre de archivo original
            documento.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo))

        controlador.ActualizarProducto(id_producto, id_tipo_producto, nombre, descripcion, precio, stock, nombre_archivo)
        return jsonify({"exito":True, "msg":"El producto ha sido actualizado correctamente."})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al actualizar el producto: " + str(e)})

# Endpoint para actualizar el estado de un detalle orden
@app.route('/actualizarEstadoDetalleOrden', methods=["PUT"])
def ActualizarEstadoDetalleOrden():
    try:
        id_orden = request.form['id_orden']
        id_combo = request.form['id_combo']
        id_producto = request.form['id_producto']
        estado = request.form['estado'] # Este puede ser 'ACEPTADO' o 'RECHAZADO'
        controlador.ActualizarEstadoDetalleOrden(id_orden, id_combo, id_producto, estado)
        return jsonify({"exito":True, "msg":"Transaccion realizada correctamente."})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al realizar la transaccion: " + str(e)})

# Endpoint para descargar un archivo que este unicamente en la carpeta public
@app.route('/descargarArchivo/<nombre_archivo>', methods=['GET'])
def DescargarArchivo (nombre_archivo):
    try:
        path = "../public/" + nombre_archivo
        return send_file(path, as_attachment=True)
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error, no se ha encontrado el archivo"})

# Endpoint para obtener una lista de empresas
@app.route('/obtenerListaEmpresas', methods=['GET'])
def ObtenerListaEmpresas():
    try:
        empresas = controlador.ObtenerEmpresas()
        return jsonify({"exito":True, "empresas":empresas})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al obtener las empresas: " + str(e)})

#Endpoint para obtener los combos de una empresa
@app.route('/obtenerCombosEmpresa/<id_empresa>', methods=['GET'])
def ObtenerCombosEmpresa(id_empresa):
    try:
        combos = controlador.ObtenerlistaCombosEmpresa(id_empresa)
        return jsonify({"exito":True, "combos":combos})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al obtener los combos: " + str(e)})

#Endpoint para mostrar todos los combos existentes con su respectivo detalle
@app.route('/mostrarCombosConProductos/<id_empresa>', methods=['GET'])
def MostrarCombosConProductos(id_empresa):
    try:
        respuesta = controlador.MostrarCombosConProductos(id_empresa)
        return jsonify({"exito":True, "msg":respuesta})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al mostrar la informacion: " + str(e)})

#Endpoint para eliminar productos de una orden
@app.route('/eliminarProductoOrden/<id_producto>/<id_cliente>', methods=['DELETE'])
def EliminarProductoOrden(id_producto, id_cliente):
    try:
        if controlador.EliminarProductoCarrito(id_producto, id_cliente):
            return jsonify({"exito":True, "msg":"Se ha eliminado el producto de la orden correctamente."})
        else :
            return jsonify({'exito':False, "msg": "Error al eliminar el producto de la orden" })
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al eliminar el producto de la orden: " + str(e)})

#Endpoint para eliminar combo de una orden
@app.route('/eliminarComboOrden/<id_combo>/<id_cliente>', methods=['DELETE'])
def EliminarComboOrden(id_combo, id_cliente):
    try:
        if controlador.EliminarComboCarrito(id_combo, id_cliente):
            return jsonify({"exito":True, "msg":"Se ha eliminado el combo de la orden correctamente."})
        else :
            return jsonify({'exito':False, "msg": "Error al eliminar el combo de la orden" })
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al eliminar el combo de la orden: " + str(e)})

#Endpoint para confirmar una orden
@app.route('/confirmarOrden/<id_cliente>', methods=['PUT'])
def ConfirmarOrden(id_cliente):
    try:
        if controlador.ConfirmarOrdenCarrito(id_cliente):
            return jsonify({"exito":True, "msg":"Se ha confirmado la orden correctamente."})
        else :
            return jsonify({'exito':False, "msg": "Error al confirmar la orden" })
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al confirmar la orden: " + str(e)})

@app.route('/AgregarProductoCarrito', methods=['POST'])
def AgregarProductoCarrito():
    try:
        id_cliente = request.form['id_cliente']
        id_direccion = request.form['id_direccion']
        id_repartidor = request.form['id_repartidor']
        fecha = request.form['fecha']
        calificacion = request.form['calificacion']
        comentario = request.form['comentario']
        metodo_pago = request.form['metodo_pago']
        id_combo = request.form['id_combo']
        cantidad = request.form['cantidad']
        id_producto = request.form['id_producto']
        observaciones = request.form['observaciones']
        estado = request.form['estado']
        id_orden = controlador.AgregarProductoCarrito(id_cliente, id_direccion, id_repartidor, fecha, calificacion, comentario, metodo_pago)
        controlador.AgregarDetalleOrden(id_combo, id_orden, cantidad, id_producto, observaciones, estado)
        return jsonify({"exito":True, "msg":"Se ha agregado el producto al carrito correctamente."})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al agregar el producto al carrito: " + str(e)})

#Endpoint para mostrar el carrito de un cliente
@app.route('/mostrarCarritoProductos/<id_cliente>', methods=['GET'])
def MostrarCarritoCliente(id_cliente):
    try:
        carrito = controlador.MostrarCarrito(id_cliente)
        return jsonify({"exito":True, "carrito":carrito})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al mostrar el carrito: " + str(e)})

#Endpoint para mostrar el carrito de un cliente
@app.route('/mostrarCarritoCombos/<id_cliente>', methods=['GET'])
def MostrarComboCarritoCliente(id_cliente):
    try:
        carrito = controlador.MostrarCarritoCombos(id_cliente)
        return jsonify({"exito":True, "carrito":carrito})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al mostrar el carrito: " + str(e)})

#Endpoint para mostrar el carrito de un cliente
@app.route('/mostrarProductosCombo/<id_combo>', methods=['GET'])
def MostrarProductosCombo(id_combo):
    try:
        carrito = controlador.MostrarProductosDeUnCombo(id_combo)
        return jsonify({"exito":True, "carrito":carrito})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al mostrar el carrito: " + str(e)})


@app.route('/ModificarProductoCarrito', methods=['PUT'])
def ModificarProductoCarrit():
    try:
        id_cliente = request.form['id_cliente']
        id_direccion = request.form['id_direccion']
        id_repartidor = request.form['id_repartidor']
        fecha = request.form['fecha']
        calificacion = request.form['calificacion']
        comentario = request.form['comentario']
        metodo_pago = request.form['metodo_pago']
        cantidad = request.form['cantidad']
        id_producto = request.form['id_producto']
        observaciones = request.form['observaciones']
        id_orden = controlador.ModificarProductoCarrito(id_cliente, id_direccion, id_repartidor, fecha, calificacion, comentario, metodo_pago)
        controlador.ModificarDetalleOrdenProducto(id_orden, id_producto, cantidad, observaciones)
        return jsonify({"exito":True, "msg":"Se ha modificado el producto del carrito correctamente."})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al modificar el producto del carrito: " + str(e)})


@app.route('/ModificarComboCarrito', methods=['PUT'])
def ModificarComboCarrit():
    try:
        id_cliente = request.form['id_cliente']
        id_direccion = request.form['id_direccion']
        id_repartidor = request.form['id_repartidor']
        fecha = request.form['fecha']
        calificacion = request.form['calificacion']
        comentario = request.form['comentario']
        metodo_pago = request.form['metodo_pago']
        id_combo = request.form['id_combo']
        cantidad = request.form['cantidad']
        observaciones = request.form['observaciones']
        id_orden = controlador.ModificarComboCarrito(id_cliente, id_direccion, id_repartidor, fecha, calificacion, comentario, metodo_pago)
        controlador.ModificarDetalleOrdenCombo(id_orden, id_combo, cantidad, observaciones)
        return jsonify({"exito":True, "msg":"Se ha modificado el combo del carrito correctamente."})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al modificar el combo del carrito: " + str(e)})

# Endpoint para ver los pedidos pendientes de asignacion de repartidor
@app.route('/VerPedidosPendientesRepartidor', methods=['GET'])
def VerPedidosPendientesRepartidor():
    try:
        pedidos = controlador.VerPedidosPendientesRepartidor()
        return jsonify({"exito":True, "pedidos":pedidos})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al mostar los pedidos pendientes de asignacion de repartidor: " + str(e)})   

# Endpoint para ver el pedido el asignado del repartidor
@app.route('/VerPedidoAsignadoRepartidor/<nombre>', methods=['GET'])
def VerPedidoAsignadoRepartidor(nombre):
    try:
        pedidos = controlador.VerPedidoAsignadoRepartidor(nombre)
        return jsonify({"exito":True, "pedidos":pedidos})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al mostar el pedido asignado del repartidor: " + str(e)})   

# Endpoint para cambiar el estado del pedido a "EN PROCESO" cuando un repartidor se lo asigna
@app.route('/AsignarPedidoRepartidor', methods=['PUT'])
def AsignarPedidoRepartidor():
    try:
        pet = request.json
        id_ord = pet[0]
        user_rep = pet[1]
        controlador.AsignarPedidoRepartidor(id_ord, user_rep)
        return jsonify({"exito":True, "msj":"Pedido asignado exitosamente"})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al asignar el pedido al repartidor: " + str(e)}) 

# Endpoint para cambiear el estado del pedido a "ENTREGADO" cuando el repartidor lo entrega
@app.route('/EntregarPedidoRepartidor', methods=['PUT'])
def EntregarPedidoRepartidor():
    try:
        resp = request.json
        ord_id = resp[0]
        usuario = resp[1]
        controlador.EntregarPedidoRepartidor(ord_id, usuario)
        return jsonify({"exito":True, "msj":"Pedido entregado exitosamente"})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al marcar el pedido como 'ENTREGADO': " + str(e)}) 

@app.route('/VerTiposProductos', methods=['GET'])
def VerTiposProduct():
    try:
        tipos = controlador.VerTiposProductos()
        return jsonify({"exito":True, "tipos":tipos})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al mostar los tipos de productos: " + str(e)})


@app.route('/VerEmpresasPorTipo/<tipo>', methods=['GET'])
def VerEmpresasPorTip(tipo):
    try:
        empresas = controlador.VerEmpresasPorTipo(tipo)
        print(empresas)
        return jsonify({"exito":True, "empresas":empresas})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al mostar las empresas por tipo: " + str(e)})

@app.route('/VerCombosPorProducto/<id_producto>', methods=['GET'])
def VerCombosPorProduct(id_producto):
    try:
        combos = controlador.VerCombosPorProducto(id_producto)
        return jsonify({"exito":True, "combos":combos})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al mostar los combos por producto: " + str(e)})

#Endpoint para ver los combos por el tipo de producto
@app.route('/VerCombosPorTipoProducto/<tipo>', methods=['GET'])
def VerCombosPorTipoProduct(tipo):
    try:
        combos = controlador.VerCombosPorTipo(tipo)
        return jsonify({"exito":True, "combos":combos})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al mostar los combos por tipo de producto: " + str(e)})



#Endpoint para ver los datos del repartidor logueado
@app.route('/VerPerfilRepartidor/<usuario>', methods=['GET'])
def VerPerfilRepartidor(usuario):
    try:
        mes_actual = datetime.now().month
        perfil = controlador.VerPerfilRepartidor(usuario, mes_actual)
        return jsonify({"exito":True, "repartidor":perfil})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al mostar los datos del repartidor logueado: " + str(e)})

#Endpoint para ver toda las ordenes de un cliente
@app.route('/VerOrdenesCliente/<id_cliente>', methods=['GET'])
def VerOrdenesClient(id_cliente):
    try:
        ordenes = controlador.VerOrdenesCliente(id_cliente)
        return jsonify({"exito":True, "ordenes":ordenes})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al mostar las ordenes del cliente: " + str(e)})

#Endpoint para actualizar el comentario y la calificacion de una orden
@app.route('/ActualizarComentarioCalificacion', methods=['PUT'])
def ActualizarComentarioCalificacionOrden():
    try:        
        id_orden = request.form['id_orden']
        comentario = request.form['comentario']
        calificacion = request.form['calificacion']
        controlador.ActualizarOrden(id_orden, comentario, calificacion)
        return jsonify({"exito":True, "msj":"Comentario y calificacion actualizados exitosamente"})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al actualizar el comentario y la calificacion: " + str(e)})

#Endpoint para modificar los datos del repartidor logueado
@app.route('/ActualizarPerfilRepartidor/<usuario>', methods=['PUT'])
def ActualizarPerfilRepartidor(usuario):
    try:
        data = request.json
        correo = data[0]
        contrasena = data[1]
        nit = data[2]
        telefono = data[3]
        municipio = data[4]
        lugar = data[5]
        transporte = data[6]
        licencia = data[7]
        nombre_archivo = None
        if('documento' in request.files):
            documento = request.files['documento']
            filename = secure_filename(documento.filename)
            if(not archivo_permitido(filename)):
                return jsonify({"exito":False, "msg":"La extensión del archivo no esta permitido"})
            hora_actual = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") # Obtiene la hora actual como una cadena en el formato "YYYY-MM-DD-HH-MM-SS"
            nombre_archivo = hora_actual + '_' + filename # Concatena la hora actual y el nombre de archivo original
            documento.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo))

        controlador.ActualizarPerfilRepartidor(correo, contrasena, nit, telefono, municipio, lugar, transporte, licencia, nombre_archivo)
        return jsonify({'exito':True, "msj": "Se actualizo correctamente el perfil del repartidor"})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al modificar los datos del repartidor logueado: " + str(e)})



#Endpoint para ver todos los pedidos entregados por el repartidor
@app.route('/VerPedidosEntregadosRepartidor/<usuario>', methods=['GET'])
def VerPedidosEntregadosRepartidor(usuario):
    try:
        ordenes = controlador.VerPedidosEntregadosRepartidor(usuario)
        return jsonify({"exito":True, "ordenes":ordenes})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al mostar las ordenes del cliente: " + str(e)})


#Endpoint para obtener el ultimo combo insertado
@app.route('/VerUltimoComboInsertado', methods=['GET'])
def VerUltimoCombo():
    try:
        combo = controlador.VerUltimoComboInsertado()
        return jsonify({"exito":True, "combo":combo})
    except Exception as e:
        return jsonify({'exito':False, "msg": "Error al mostar el ultimo combo: " + str(e)})

if __name__ == '__main__':
    print("SERVIDOR INICIADO EN EL PUERTO: 5000")

    # serve(app, port=5000)
    app.run(debug=True)
