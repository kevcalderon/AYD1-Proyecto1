import React, { useState } from "react";
import NavBar from "../../Navbars/NavbarU";
import Container from "react-bootstrap/Container";

import { FormProvider, useForm } from "react-hook-form";
import { Button, Form } from "react-bootstrap";
import FormInput from "../../form-input/FormInput";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useNavigate } from "react-router-dom";
import API_URL from "../../../app/constants";

function Login() {
  const navigate = useNavigate();
  const [mostrarAlert, setMostrarAlert] = useState(false);
  const validationSchema = z.object({
    nombre_empresa: z.string().min(1, { message: "Campo Obligatorio" }),
    contrasenia: z.string().min(1, { message: "Campo Obligatorio" }),
  });

  const methods = useForm({
    resolver: zodResolver(validationSchema),
  });

  const {
    handleSubmit,
    register,
    formState: { errors },
  } = methods;

  function mostrarComponente() {
    setMostrarAlert(true);
    setTimeout(() => setMostrarAlert(false), 3000);
  }

  const onSubmitFormSesion = async (values) => {
    console.log(values);
    await fetch(
      `${API_URL}/loguearEmpresa/${values.nombre_empresa}/${values.contrasenia}`,
      {
        method: "GET",
      }
    )
      .then((response) => response.json())
      .then((res) => {
        console.log(res);
        if (res.respuesta !== null) {
          const empresaJSON = JSON.stringify(res.respuesta);
          localStorage.setItem("empresa", empresaJSON);
          console.log(res);
          navigate("/CrearProducto");
        } else {
          mostrarComponente();
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return (
    <div style={{ color: "white" }}>
      <NavBar />
      <Container>
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            alignContent: "center",
            alignItems: "center",
          }}
        >
          <h1 style={{ margin: "7%" }}>Login - Empresa</h1>
          <img
            src="https://cdn-icons-png.flaticon.com/512/4616/4616041.png"
            width="150px"
            height="150px"
            alt="loginImg"
          />
        </div>
        {mostrarAlert && (
          <div
            className="alert alert-dismissible alert-danger"
            style={{ margin: "3%" }}
          >
            <strong>Error!</strong> Credenciales invalidas.
          </div>
        )}
        <div>
          <FormProvider {...methods}>
            <Form onSubmit={handleSubmit(onSubmitFormSesion)}>
              <Form.Label>Username</Form.Label>
              <FormInput
                placeholder="Ingresa su username"
                errors={errors}
                name="nombre_empresa"
                controlId="idNombreEmpresa"
                type="text"
                register={register}
              />
              <Form.Label>Contraseña</Form.Label>
              <FormInput
                placeholder="Ingresa tu contraseña"
                errors={errors}
                name="contrasenia"
                controlId="idPassword"
                type="password"
                register={register}
              />
              <Button variant="warning" type="submit">
                Iniciar Sesión
              </Button>
            </Form>
          </FormProvider>
        </div>
      </Container>
    </div>
  );
}

export default Login;
