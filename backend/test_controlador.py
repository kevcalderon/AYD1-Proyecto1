from controlador import VerDepartamentos, LoguearCliente, VerTiposEmpresa, ObtenerMunicipios, ObtenerProductosEmpresaTipoProducto, AgregarDireccion, AgregarEmpresa, ObtenerProductoCombo
import pytest
from unittest import mock
from unittest.mock import MagicMock

@mock.patch('conexion.obtener_conexion')
def test_VerDepartamentos(mock_conexion):
    mock_cursor = mock_conexion.return_value.cursor.return_value
    mock_cursor.fetchall.return_value = [(1, 'Alta Verapaz'), (2, 'Baja Verapaz'), (3, 'Chimaltenango'), (4, 'Chiquimula'), (5, 'El Progreso'), (6, 'Escuintla'), (7, 'Guatemala'), (8, 'Huehuetenango'), (9, 'Izabal'), (10, 'Jalapa'), (11, 'Jutiapa'), (12, 'Petén'), (13, 'Quetzaltenango'), (14, 'Quiché'), (15, 'Retalhuleu'), (16, 'Sacatepéquez'), (17, 'San Marcos'), (18, 'Santa Rosa'), (19, 'Sololá'), (20, 'Suchitepéquez'), (21, 'Totonicapán'), (22, 'Zacapa')]
    resultado_esperado = [{'DEP_ID': 1, 'NOMBRE': 'Alta Verapaz'}, {'DEP_ID': 2, 'NOMBRE': 'Baja Verapaz'}, {'DEP_ID': 3, 'NOMBRE': 'Chimaltenango'}, {'DEP_ID': 4, 'NOMBRE': 'Chiquimula'}, {'DEP_ID': 5, 'NOMBRE': 'El Progreso'}, {'DEP_ID': 6, 'NOMBRE': 'Escuintla'}, {'DEP_ID': 7, 'NOMBRE': 'Guatemala'}, {'DEP_ID': 8, 'NOMBRE': 'Huehuetenango'}, {'DEP_ID': 9, 'NOMBRE': 'Izabal'}, {'DEP_ID': 10, 'NOMBRE': 'Jalapa'}, {'DEP_ID': 11, 'NOMBRE': 'Jutiapa'}, {'DEP_ID': 12, 'NOMBRE': 'Petén'}, {'DEP_ID': 13, 'NOMBRE': 'Quetzaltenango'}, {'DEP_ID': 14, 'NOMBRE': 'Quiché'}, {'DEP_ID': 15, 'NOMBRE': 'Retalhuleu'}, {'DEP_ID': 16, 'NOMBRE': 'Sacatepéquez'}, {'DEP_ID': 17, 'NOMBRE': 'San Marcos'}, {'DEP_ID': 18, 'NOMBRE': 'Santa Rosa'}, {'DEP_ID': 19, 'NOMBRE': 'Sololá'}, {'DEP_ID': 20, 'NOMBRE': 'Suchitepéquez'}, {'DEP_ID': 21, 'NOMBRE': 'Totonicapán'}, {'DEP_ID': 22, 'NOMBRE': 'Zacapa'}]
    departamentos_obtenidos = VerDepartamentos()
    assert resultado_esperado == departamentos_obtenidos


@mock.patch('conexion.obtener_conexion')
def test_loguear_cliente(mock_conexion):
 
    # Ejecutar la función a probar
    usuario = LoguearCliente('client1', '123')
    # Verificar el resultado
    assert usuario is None



def test_ver_tipos_empresa():
    tipos_empresa = VerTiposEmpresa()
    # Se verifica que la respuesta no sea nula y que tenga al menos un tipo de empresa
    assert tipos_empresa is not None
    assert len(tipos_empresa) > 0
    # Se verifica que cada tipo de empresa tenga los campos esperados
    for tipo_empresa in tipos_empresa:
        assert "T_EMP_ID" in tipo_empresa
        assert "NOMBRE" in tipo_empresa



def test_ObtenerMunicipios():
    with mock.patch("conexion.obtener_conexion") as mock_obtener_conexion:
        mock_cursor = mock_obtener_conexion.return_value.cursor.return_value
    
        # Llamamos a la función que vamos a testear
        municipios = ObtenerMunicipios(1)

    # Verificamos que la longitud de la respuesta sea mayor a cero
    assert len(municipios) > 0


def test_ObtenerProductosEmpresaTipoProducto():
    # Se prueba que la función retorne al menos un producto cuando se le pasa un id de empresa y un id de tipo de producto válidos
    productos = ObtenerProductosEmpresaTipoProducto(1, 1)
    assert len(productos) > 0
  


def test_agregar_direccion():
    # Agregar una dirección nueva
    direccion_id = AgregarDireccion(1, "Calle 123")
    assert direccion_id > 0
    

def test_agregar_empresa():
    # Agregar una empresa nueva
    empresa_id = AgregarEmpresa(1, 1, "Mi empresa", "Descripción de mi empresa", "correo@miempresa.com", "1234567", "miusuario", "micontrasenia", "1234567-8", "documento.pdf")
    assert empresa_id > 0
    

def test_obtener_producto_combo():
    with mock.patch('conexion.obtener_conexion'):
        # Simulamos que la conexión se realizó correctamente
        ids_producto = ObtenerProductoCombo(1)
        assert len(ids_producto) > 0