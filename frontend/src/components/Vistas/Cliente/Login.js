import { React, useState } from "react";
import NavBar from "../../Navbars/NavbarU";
import { Form, Button } from "react-bootstrap";
import { Icon } from "@iconify/react";
import IconoLogin from "@iconify-icons/mdi/login";
import API_URL from "../../../app/constants";
import { useNavigate } from "react-router-dom";

function Login() {
  const [usuario, setUsuario] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      await fetch(`${API_URL}/loguearCliente/${usuario}/${password}`, {
        method: "GET",
      })
        .then((response) => response.json())
        .then((res) => {
          console.log(res);
          if (res.respuesta !== null) {
            const clienteJSON = JSON.stringify(res.respuesta);
            localStorage.setItem("cliente", clienteJSON);
            console.log(res);
            navigate("/Empresas");
            localStorage.removeItem("carrito");
          } else {
            alert("Usuario o contraseña incorrectos");
          }
        })
        .catch((error) => {
          console.log(error);
        });
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <>
      <NavBar />
      <div
        className="d-flex flex-column align-items-center"
        style={{ color: "white" }}
      >
        <div className="mt-3">
          <Icon icon={IconoLogin} style={{ fontSize: "3rem" }} />
          <h2 className="mt-3">LOGIN</h2>
        </div>
        <Form onSubmit={handleLogin} className="mt-4">
          <Form.Group controlId="formBasicUsername">
            <Form.Label>Nombre de Usuario</Form.Label>
            <Form.Control
              type="text"
              placeholder="Ingrese su nombre de usuario"
              value={usuario}
              onChange={(e) => setUsuario(e.target.value)}
            />
          </Form.Group>

          <Form.Group controlId="formBasicPassword">
            <Form.Label>Contraseña</Form.Label>
            <Form.Control
              type="password"
              placeholder="Ingrese su contraseña"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </Form.Group>

          <Button variant="primary" type="submit" className="mt-3">
            Iniciar sesión
          </Button>
        </Form>
      </div>
    </>
  );
}

export default Login;
