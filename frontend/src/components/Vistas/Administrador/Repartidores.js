import React, { useEffect } from "react";
import NavBar from "../../Navbars/NavbarA";
import Tab from "react-bootstrap/Tab";
import Tabs from "react-bootstrap/Tabs";
import { Container } from "react-bootstrap";
import API_URL from "../../../app/constants";

function Repartidores() {
  const getRepartidores = async () => {
    await fetch(`${API_URL}/VerSolicitudesRepartidores`, {
      method: "GET",
    })
      .then((response) => response.json())
      .then((res) => {
        console.log(res);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  useEffect(() => {
    getRepartidores();
  }, []);

  return (
    <div>
      <NavBar />
      <br></br>
      <Container>
        <Tabs
          defaultActiveKey="Solicitudes"
          id="uncontrolled-tab-example"
          className="mb-3"
          style={{ backgroundColor: "gray", color: "green" }}
        >
          <Tab eventKey="Solicitudes" title="Solicitudes">
            Tab content for Home
          </Tab>
          <Tab eventKey="Deshabilitar" title="Deshabilitar">
            Tab content for Profile
          </Tab>
        </Tabs>
      </Container>
    </div>
  );
}

export default Repartidores;
