from conexion import obtener_conexion
import controlador
from flask import Flask, jsonify, request, Response, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime
import os

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
def inicioSesionProveedor(USER, CONTRA):
    try:
        proveedor=controlador.VerificarSesProveedor(USER, CONTRA)
        if  proveedor != None:
            return jsonify({'exito':True, "respuesta":proveedor})
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

if __name__ == '__main__':
    print("SERVIDOR INICIADO EN EL PUERTO: 5000")

    # serve(app, port=5000)
    app.run(debug=True)
