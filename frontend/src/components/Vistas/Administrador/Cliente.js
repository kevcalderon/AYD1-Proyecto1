import React, { useEffect, useState } from "react";
import NavBar from "../../Navbars/NavbarA";
import { Button, Container, Tab, Table, Tabs } from "react-bootstrap";
import API_URL from "../../../app/constants";

function Cliente() {
  const [clientes, setClientes] = useState([]);

  const getClientes = async () => {
    await fetch(`${API_URL}/VerClientesAdmin`, {
      method: "GET",
    })
      .then((response) => response.json())
      .then((res) => {
        console.log(res);
        setClientes(res.clientes);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const deshabilitarClientes = async (idCliente) => {
    await fetch(`${API_URL}/DeshabilitarCliente/${idCliente}`, {
      method: "PUT",
    })
      .then((response) => response.json())
      .then((res) => {
        console.log(res);
        getClientes();
      })
      .catch((error) => {
        console.log(error);
      });
  };

  useEffect(() => {
    getClientes();
  }, []);

  return (
    <div style={{ color: "white" }}>
      <NavBar />
      <br></br>
      <Container>
        <Tabs
          defaultActiveKey="Deshabilitar"
          id="uncontrolled-tab-example"
          className="mb-3"
          style={{ backgroundColor: "gray", color: "green" }}
        >
          <Tab eventKey="Deshabilitar" title="Deshabilitar">
            <Table striped bordered hover>
              <thead>
                <tr>
                  <th>#</th>
                  <th>APELLIDO</th>
                  <th>NOMBRE</th>
                  <th>CORREO</th>
                  <th>USUARIO</th>
                  <th>OPCIONES</th>
                </tr>
              </thead>
              <tbody>
                {clientes.map((cliente, index) => {
                  return (
                    <tr key={index}>
                      <td>{cliente.CLI_ID}</td>
                      <td>{cliente.APELLIDO}</td>
                      <td>{cliente.NOMBRE}</td>
                      <td>{cliente.CORREO}</td>
                      <td>{cliente.USUARIO}</td>
                      <td>
                        <Button
                          variant="danger"
                          onClick={() => deshabilitarClientes(cliente.CLI_ID)}
                        >
                          Deshabilitar
                        </Button>
                      </td>
                    </tr>
                  );
                })}
                {/* <tr>
                  <td>1</td>
                  <td>Mark</td>
                  <td>Otto</td>
                  <td>@mdo</td>
                </tr> */}
              </tbody>
            </Table>
          </Tab>
        </Tabs>
      </Container>
    </div>
  );
}

export default Cliente;
