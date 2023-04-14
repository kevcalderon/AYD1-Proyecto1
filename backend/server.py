from conexion import obtener_conexion
import controlador
from flask import Flask, jsonify, request, Response
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

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

if __name__ == '__main__':
    print("SERVIDOR INICIADO EN EL PUERTO: 5000")
    
    # serve(app, port=5000)
    app.run(debug=True)
