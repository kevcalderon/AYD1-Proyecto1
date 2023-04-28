import React, { useEffect, useState } from "react";
import NavBar from "../../Navbars/NavbarA";
import API_URL from "../../../app/constants";
import { Button, Container, Tab, Table, Tabs } from "react-bootstrap";

function Empresa() {
  const [empresaSolicitudes, setEmpresasSolicitudes] = useState([]);
  const [empresasDesh, setEmpresasDesh] = useState([]);

  const getEmpresasSolicitudes = async () => {
    await fetch(`${API_URL}/VerSolicitudesEmpresas`, {
      method: "GET",
    })
      .then((response) => response.json())
      .then((res) => {
        console.log(res);
        setEmpresasSolicitudes(res.solicitudes);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const getEmpresasDeshabilitar = async () => {
    await fetch(`${API_URL}/VerEmpresasAdmin`, {
      method: "GET",
    })
      .then((response) => response.json())
      .then((res) => {
        console.log(res);
        setEmpresasDesh(res.empresas);
        // setEmpresasDesh()
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const habilitarEmpresa = async (idSolicitud) => {
    await fetch(`${API_URL}/AceptarSolicitud/${idSolicitud}`, {
      method: "PUT",
    })
      .then((response) => response.json())
      .then((res) => {
        alert(res.exito);
        console.log(res);
        getEmpresasSolicitudes();
        // setEmpresasDesh()
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const rechazarEmpresa = async (idSolicitud) => {
    await fetch(`${API_URL}/RechazarSolicitud/${idSolicitud}`, {
      method: "PUT",
    })
      .then((response) => response.json())
      .then((res) => {
        alert(res.exito);
        console.log(res);
        getEmpresasSolicitudes();
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const deshabilitarEmpresa = async (idEmpresa) => {
    await fetch(`${API_URL}/DeshabilitarEmpresa/${idEmpresa}`, {
      method: "PUT",
    })
      .then((response) => response.json())
      .then((res) => {
        alert(res.exito);
        console.log(res);
        getEmpresasDeshabilitar();
      })
      .catch((error) => {
        console.log(error);
      });
  };

  useEffect(() => {
    getEmpresasSolicitudes();
    getEmpresasDeshabilitar();
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
          style={{ backgroundColor: "skyblue", color: "green" }}
        >
          <Tab eventKey="Deshabilitar" title="Deshabilitar">
            <Table striped bordered hover>
              <thead>
                <tr>
                  <th>#</th>
                  <th>NOMBRE</th>
                  <th>TIPO</th>
                  <th>USUARIO</th>
                  <th>NIT</th>
                  <th>OPCIONES</th>
                </tr>
              </thead>
              <tbody>
                {empresasDesh.map((empresa, index) => {
                  return (
                    <tr key={index}>
                      <td>{empresa.EMP_ID}</td>
                      <td>{empresa.NOMBRE}</td>
                      <td>{empresa.TIPO_EMPRESA}</td>
                      <td>{empresa.USUARIO}</td>
                      <td>{empresa.NIT}</td>
                      <td>
                        <Button
                          variant="danger"
                          onClick={() => deshabilitarEmpresa(empresa.EMP_ID)}
                        >
                          Deshabilitar
                        </Button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </Table>
          </Tab>
          <Tab eventKey="Solicitudes" title="Solicitudes">
            <Table striped bordered hover>
              <thead>
                <tr>
                  <th>#</th>
                  <th>NOMBRE</th>
                  <th>TIPO SOLICITUD</th>
                  <th>CORREO</th>
                  <th>OPCIONES</th>
                </tr>
              </thead>
              <tbody>
                {empresaSolicitudes.map((cliente, index) => {
                  return (
                    <tr key={index}>
                      <td>{cliente.EMP_ID}</td>
                      <td>{cliente.NOMBRE}</td>
                      <td>{cliente.TIPO_SOLICITUD}</td>
                      <td>{cliente.CORREO}</td>
                      <td>
                        <Button
                          variant="success"
                          onClick={() => habilitarEmpresa(cliente.SOL_ID)}
                        >
                          Habilitar
                        </Button>
                        <Button
                          variant="danger"
                          onClick={() => rechazarEmpresa(cliente.SOL_ID)}
                        >
                          Rechazar
                        </Button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </Table>
          </Tab>
        </Tabs>
      </Container>
    </div>
  );
}

export default Empresa;
