import React, { useEffect, useState } from "react";
import axios from "axios";
import NavBar from "../../Navbars/NavbarA";
import { Divider, Header, Table } from 'semantic-ui-react';
import API_URL from "../../../app/constants";

function Reportes(props) {
  const [ventas, setVentas] = useState([]);
  const [ventas2, setVentas2] = useState([]);
  const [ventas3, setVentas3] = useState([]);
  const [usuarios, setUsuarios] = useState([]);
  const [usuarios1, setUsuarios1] = useState([]);
  const [repartidores, setRepartidores] = useState([]);
  const [repartidores1, setRepartidores1] = useState([]);
  useEffect(() => {
    axios
      .get(`${API_URL}/Ventas1`)
      .then((res) => {
        setVentas(res.data.msg);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  useEffect(() => {
    axios
      .get(`${API_URL}/Ventas2`)
      .then((res) => {
        setVentas2(res.data.msg);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  useEffect(() => {
    axios
      .get(`${API_URL}/ProductosVendidos`)
      .then((res) => {
        setVentas3(res.data.msg);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);
  useEffect(() => {
    axios
      .get(`${API_URL}/TotalClientes`)
      .then((res) => {
        setUsuarios(res.data.msg);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);
  useEffect(() => {
    axios
      .get(`${API_URL}/ClientesActivos`)
      .then((res) => {
        setUsuarios1(res.data.msg);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);
  useEffect(() => {
    axios
      .get(`${API_URL}/PedidosRepartidor`)
      .then((res) => {
        setRepartidores(res.data.msg);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  useEffect(() => {
    axios
      .get(`${API_URL}/PromedioCalificacionRepartidor`)
      .then((res) => {
        setRepartidores1(res.data.msg);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  return (
    <div style={{ color: "white" }}>
      <NavBar />
      <h1>Reportes</h1>
      <br />
      <h3>Reporte de ventas</h3>
      <br />
      <Divider></Divider>
      <h4>Numero de Pedidos</h4>
      <Table celled padded>
        <Table.Header>
          <Table.Row>
            <Table.HeaderCell>ID</Table.HeaderCell>
            <Table.HeaderCell>Empresa</Table.HeaderCell>
            <Table.HeaderCell>Total</Table.HeaderCell>
          </Table.Row>
        </Table.Header>

        <Table.Body>
          {ventas.map((venta) => (
            <Table.Row>
              <Table.Cell>
                <Header textAlign='center'>
                  {venta.id}
                </Header>
              </Table.Cell>
              <Table.Cell>
                <Header textAlign='center'>
                  {venta.empresa}
                </Header>
              </Table.Cell>
              <Table.Cell>
                <Header textAlign='center'>
                  {venta.total}
                </Header>
              </Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table>
      <Divider></Divider>
      <h4>Valor de las ventas</h4>
      <Table celled padded>
        <Table.Header>
          <Table.Row>
            <Table.HeaderCell>ID</Table.HeaderCell>
            <Table.HeaderCell>Total</Table.HeaderCell>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {ventas2.map((venta2) => (
            <Table.Row>
              <Table.Cell>
                <Header textAlign='center'>
                  {venta2.id}
                </Header>
              </Table.Cell>
              <Table.Cell>
                <Header textAlign='center'>
                  {venta2.total}
                </Header>
              </Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table>
      <Divider></Divider>
      <h4>Productos mas vendidos</h4>
      <Table celled padded>
        <Table.Header>
          <Table.Row>
            <Table.HeaderCell>ID</Table.HeaderCell>
            <Table.HeaderCell>Producto</Table.HeaderCell>
            <Table.HeaderCell>Total</Table.HeaderCell>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {ventas3.map((vent1a) => (
            <Table.Row>
              <Table.Cell>
                <Header textAlign='center'>
                  {vent1a.id}
                </Header>
              </Table.Cell>
              <Table.Cell>
                <Header textAlign='center'>
                  {vent1a.nombre}
                </Header>
              </Table.Cell>
              <Table.Cell>
                <Header textAlign='center'>
                  {vent1a.total}
                </Header>
              </Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table>
      <br />
      <Divider></Divider>
      <h3>Reporte de Usuarios</h3>
      <Divider></Divider>
      <h4>Cantidad de usuarios registrados</h4>
      <Table celled padded>
        <Table.Header>
          <Table.Row>
            <Table.HeaderCell>Total</Table.HeaderCell>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {usuarios.map((usuarios1) => (
            <Table.Row>
              <Table.Cell>
                <Header textAlign='center'>
                  {usuarios1.total}
                </Header>
              </Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table>
      <Divider></Divider>
      <h4>Cantidad de usuarios activos</h4>
      <Table celled padded>
        <Table.Header>
          <Table.Row>
            <Table.HeaderCell>Total</Table.HeaderCell>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {usuarios1.map((usuarios11) => (
            <Table.Row>
              <Table.Cell>
                <Header textAlign='center'>
                  {usuarios11.total}
                </Header>
              </Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table>
      <br />
      <h3>Reporte de Repartidores</h3>
      <br />
      <Divider></Divider>
      <Table celled padded>
        <Table.Header>
          <Table.Row>
            <Table.HeaderCell>Id Repartidor</Table.HeaderCell>
            <Table.HeaderCell>Nombre</Table.HeaderCell>
            <Table.HeaderCell>Cantidad de Pedidos</Table.HeaderCell>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {repartidores.map((repartidores11) => (
            <Table.Row>
              <Table.Cell>
                <Header textAlign='center'>
                  {repartidores11.id}
                </Header>
              </Table.Cell>
              <Table.Cell>
                <Header textAlign='center'>
                  {repartidores11.nombre}
                </Header>
              </Table.Cell>
              <Table.Cell>
                <Header textAlign='center'>
                  {repartidores11.total}
                </Header>
              </Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table>
      <h3>Calificacion del Repartidor</h3>
      <br />
      <Divider></Divider>
      <Table celled padded>
        <Table.Header>
          <Table.Row>
            <Table.HeaderCell>Id Repartidor</Table.HeaderCell>
            <Table.HeaderCell>Nombre</Table.HeaderCell>
            <Table.HeaderCell>Promedio Calificacion</Table.HeaderCell>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {repartidores1.map((repartidores111) => (
            <Table.Row>
              <Table.Cell>
                <Header textAlign='center'>
                  {repartidores111.id}
                </Header>
              </Table.Cell>
              <Table.Cell>
                <Header textAlign='center'>
                  {repartidores111.nombre}
                </Header>
              </Table.Cell>
              <Table.Cell>
                <Header textAlign='center'>
                  {repartidores111.promedio}
                </Header>
              </Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table>
    </div>

    
  );
}

export default Reportes;
