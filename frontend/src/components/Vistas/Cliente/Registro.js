import { React, useState, useEffect } from 'react'
import NavBar from "../../Navbars/NavbarU";
import { Form, Button, Row, Col } from 'react-bootstrap';
import { Icon } from '@iconify/react';
import registroIcon from '@iconify-icons/mdi/account-plus';
import API_URL from "../../../app/constants";

function Registro() {
  const [nombre, setNombre] = useState('');
  const [apellido, setApellido] = useState('');
  const [usuario, setUsuario] = useState('');
  const [contraseña, setContraseña] = useState('');
  const [correo, setCorreo] = useState('');
  const [telefono, setTelefono] = useState('');
  const [nit, setNit] = useState('');
  const [departamento, setDepartamento] = useState('');
  const [municipio, setMunicipio] = useState('');
  const [lugar, setLugar] = useState('');
  const [tarjeta, setTarjeta] = useState('');


  const [departamentos, setDepartamentos] = useState([]);
  const [municipios, setMunicipios] = useState([]);
  const [mostrarAlert, setMostrarAlert] = useState(false);
  const [msg, setMsg] = useState("");

  const handleRegistro = async (e) => {
    e.preventDefault();

    var json = {
      nombre: nombre,
      apellido: apellido,
      usuario: usuario,
      contra: contraseña,
      correo: correo,
      telefono: telefono,
      nit: nit,
      id_dep: departamento,
      id_muni: municipio,
      lugar: lugar,
      tarjeta: tarjeta
    }

    console.log(json);

    await fetch(`${API_URL}/registrarCliente`, {
      method : 'POST',
      headers : {
        'Content-Type' : 'application/json'
      },
      body : JSON.stringify(json)
    })
    .then((response) => response.json())
    .then((res) => {
      if (res.status === "success") {
        alert(res.message); 
        window.location.href = "/LoginCliente";
      } else {
        alert(res.message);
      }
    });
  };


  function mostrarComponente(msgAlert) {
    setMostrarAlert(true);
    setMsg(msgAlert);
    setTimeout(() => setMostrarAlert(false), 5000);
  }


  const getDepartamentos = async () => {
    await fetch(`${API_URL}/mostrarDepartamentos`)
      .then((response) => response.json())
      .then((res) => {
        setDepartamentos(res);
      });
  };

  const handleSelect = async (value) => {
    await fetch(`${API_URL}/mostrarMunicipios/${value}`)
      .then((response) => response.json())
      .then((res) => {
        console.log(res);
        setMunicipios(res);
      });
  };

  useEffect(() => {
    getDepartamentos();
  }, []);

  return (
    <>
      <NavBar />
      <div className="d-flex flex-column align-items-center" style={{ color: "black" }}>
        <div className="mt-3">
          <Icon icon={registroIcon} style={{ fontSize: '3rem' }} />
          <h2 className="mt-3">REGISTRO DE CLIENTE</h2>
        </div>
        <Form onSubmit={handleRegistro} className="mt-4">
          <Row>
            <Col>
              <Form.Group controlId="formBasicNombre">
                <Form.Label>Nombre</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Ingrese su nombre"
                  value={nombre}
                  onChange={(e) => setNombre(e.target.value)}
                />
              </Form.Group>

              <Form.Group controlId="formBasicApellido">
                <Form.Label>Apellido</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Ingrese su apellido"
                  value={apellido}
                  onChange={(e) => setApellido(e.target.value)}
                />
              </Form.Group>

              <Form.Group controlId="formBasicUsuario">
                <Form.Label>Usuario</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Ingrese su usuario"
                  value={usuario}
                  onChange={(e) => setUsuario(e.target.value)}
                />
              </Form.Group>

              <Form.Group controlId="formBasicContraseña">
                <Form.Label>Contraseña</Form.Label>
                <Form.Control
                  type="password"
                  placeholder="Ingrese su contraseña"
                  value={contraseña}
                  onChange={(e) => setContraseña(e.target.value)}
                />
              </Form.Group>

            </Col>
            <Col>

              <Form.Group controlId="formBasicCorreo">
                <Form.Label>Correo</Form.Label>
                <Form.Control
                  type="email"
                  placeholder="Ingrese su correo"
                  value={correo}
                  onChange={(e) => setCorreo(e.target.value)}
                />
              </Form.Group>

              <Form.Group controlId="formBasicTelefono">
                <Form.Label>Teléfono</Form.Label>
                <Form.Control
                  type="tel"
                  placeholder="Ingrese su teléfono"
                  value={telefono}
                  onChange={(e) => setTelefono(e.target.value)}
                />
              </Form.Group>

              <Form.Group controlId="formBasicNit">
                <Form.Label>NIT</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Ingrese su número de NIT"
                  value={nit}
                  onChange={(e) => setNit(e.target.value)}
                />
              </Form.Group>

            </Col>
            <Col>

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

              <Form.Group controlId="formBasicLugar">
                <Form.Label>Lugar</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Ingrese su lugar de residencia"
                  value={lugar}
                  onChange={(e) => setLugar(e.target.value)}
                />
              </Form.Group>

              <Form.Group controlId="formBasicTarjeta">
                <Form.Label>Tarjeta de crédito/débito</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Ingrese su número de tarjeta de crédito"
                  value={tarjeta}
                  onChange={(e) => setTarjeta(e.target.value)}
                />
              </Form.Group>
            </Col>
          </Row>
          <Button variant="warning" type="submit" style={{ marginTop: "20px", width: "20%" }}>
            Registrarse
          </Button>

        </Form>

      </div>
    </>
  )
}

export default Registro