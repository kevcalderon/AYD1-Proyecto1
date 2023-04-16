from conexion import obtener_conexion
import controlador
from flask import Flask, jsonify, request, Response
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

if __name__ == '__main__':
    print("SERVIDOR INICIADO EN EL PUERTO: 5000")

    # serve(app, port=5000)
    app.run(debug=True)
