import React, { useState, useEffect } from 'react';
import NavbarC from '../../Navbars/NavbarC';
import { Container, Button, Form } from 'react-bootstrap';
import Table from 'react-bootstrap/Table';
import API_URL from "../../../app/constants";

function compararProductos(a, b) {
  if (a.idproducto && !b.idproducto) {
    return -1;
  } else if (!a.idproducto && b.idproducto) {
    return 1;
  } else {
    return 0;
  }
}


function MiCarrito() {
  const [productos, setProductos] = useState([]);
  const [departamentos, setDepartamentos] = useState([]);
  const [municipios, setMunicipios] = useState([]);
  const [departamento, setDepartamento] = useState('');
  const [municipio, setMunicipio] = useState('');

  const [datosEntrega, setDatosEntrega] = useState({
    departamento: '',
    municipio: '',
    lugar: '',
    tipoPago: 'Efectivo',
    numeroTarjeta: '',
  });

  const getDepartamentos = async () => {
    await fetch(`${API_URL}/mostrarDepartamentos`)
      .then((response) => response.json())
      .then((res) => {
        setDepartamentos(res);
      });
  };


  useEffect(() => {
    getDepartamentos();
  }, []);

  const handleSelect = async (value) => {
    await fetch(`${API_URL}/mostrarMunicipios/${value}`)
      .then((response) => response.json())
      .then((res) => {
        setMunicipios(res);
      });
  };

  const eliminarProducto = (index) => {
    const nuevosProductos = [...productos];
    nuevosProductos.splice(index, 1);
    setProductos(nuevosProductos);
    localStorage.setItem('carrito', JSON.stringify(nuevosProductos));
    console.log(`Se eliminó el producto ${index + 1}`);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setDatosEntrega({
      ...datosEntrega,
      [name]: value,
    });
  };

  useEffect(() => {
    let data = JSON.parse(localStorage.getItem('carrito'));
    if (data != null) {
      setProductos(data);
    }
  }, []);


  productos.sort(compararProductos);




  const handleSubmit = (e) => {
    e.preventDefault();

    datosEntrega.departamento = departamento;
    datosEntrega.municipio = municipio;
 
    var clien = JSON.parse(localStorage.getItem("cliente")).CLI_ID;
 
    const json = {
      idcliente: clien,
      productos: productos,
      datosEntrega: datosEntrega,
      fecha: new Date().toLocaleDateString(),
    };

    console.log(JSON.stringify(json));

    if (productos.length === 0) {
      alert('No hay productos en el carrito');
      return;
    }

    fetch(`${API_URL}/AgregarProductoCarrito`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(json),
    })
      .then((response) => response.json())
      .then((res) => {
        if( res.exito){
          alert('Pedido realizado con éxito');
          localStorage.removeItem('carrito'); 
      }else{
        alert('Error al realizar el pedido');
      }
      });
  };

  return (
    <div>
      <NavbarC />
      <Container style={{ marginTop: '20px', fontSize: '20px' }}>
        <h2>Mi Carrito</h2>
        <p>Agrega la cantidad de productos que necesitas y confirma el pedido</p>
      </Container>
      <Container style={{ backgroundColor: 'white', padding: '20px', marginTop: '20px' }}>
        <Table striped bordered hover size="sm" style={{ marginTop: '10px' }}>
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Tipo</th>
              <th>Cantidad</th>
              <th>Observación</th>
              <th>Opciones</th>
            </tr>
          </thead>
          <tbody>
            {productos.map((producto, index) => (
              <tr key={index}>
                <td>{producto.nombre}</td>
                <td>{producto.tipo}</td>
                <td>
                  <input
                    type="number"
                    value={producto.cantidad}
                    max={producto.stock}
                    onChange={(e) => {
                      const nuevosProductos = [...productos];
                      nuevosProductos[index].cantidad = e.target.value;
                      setProductos(nuevosProductos);
                    }}
                  />
                </td>
                <td>
                  <input
                    type="text"
                    placeholder='Observación por producto'
                    value={producto.observacion}
                    onChange={(e) => {
                      const nuevosProductos = [...productos];
                      nuevosProductos[index].observacion = e.target.value;
                      setProductos(nuevosProductos);
                    }}
                  />
                </td>
                <td>
                  <Button variant="danger" onClick={() => eliminarProducto(index)}>
                    Eliminar
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
        <hr />
        <h2>Datos de entrega</h2>
        <Form onSubmit={handleSubmit}>

          <Form.Group controlId="formBasicDepartamento">
            <Form.Label>Departamento</Form.Label>
            <Form.Select
              name="departamento"
              onChange={(e) => {
                handleSelect(e.target.value);
                setDepartamento(e.target.value);
              }}
            >
              {departamentos.map((departamento) => {
                return (
                  <option
                    key={departamento.DEP_ID}
                    value={departamento.DEP_ID}
                  >
                    {departamento.NOMBRE}
                  </option>
                );
              })}
            </Form.Select>

          </Form.Group>

          <Form.Group controlId="formBasicMunicipio">
            <Form.Label>Municipio</Form.Label>
            <Form.Select name="municipio"
              onChange={(e) => setMunicipio(e.target.value)}
            >
              {municipios.length === 0
                ? ""
                : municipios.map((municipio) => {
                  return (
                    <option key={municipio.MUN_ID} value={municipio.MUN_ID}>
                      {municipio.NOMBRE_MUNICIPIO}
                    </option>
                  );
                })}
            </Form.Select>
          </Form.Group>

          <Form.Group controlId="lugar">
            <Form.Label>Lugar de entrega</Form.Label>
            <Form.Control type="text" name="lugar" value={datosEntrega.lugar} onChange={handleChange} />
          </Form.Group>

          <Form.Group controlId="tipoPago">
            <Form.Label>Tipo de pago</Form.Label>
            <Form.Control as="select" name="tipoPago" value={datosEntrega.tipoPago} onChange={handleChange}>
              <option>Efectivo</option>
              <option>Tarjeta de crédito</option>
            </Form.Control>
          </Form.Group>

          {datosEntrega.tipoPago === 'Tarjeta de crédito' && (
            <Form.Group controlId="numeroTarjeta">
              <Form.Label>Número de Tarjeta</Form.Label>
              <Form.Control type="text" name="numeroTarjeta" value={datosEntrega.numeroTarjeta} onChange={handleChange} />
            </Form.Group>
          )}

          <Button variant="primary" type="submit" style={{ marginTop: '20px' }}>
            Confirmar Pedido
          </Button>
        </Form>
      </Container>
    </div>
  );
}

export default MiCarrito;