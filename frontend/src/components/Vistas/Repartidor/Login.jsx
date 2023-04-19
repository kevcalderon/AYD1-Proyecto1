import React, { useState } from "react";
import NavBar from "../../Navbars/NavbarU";
import Container from "react-bootstrap/Container";

import { FormProvider, useForm } from "react-hook-form";
import { Button, Form } from "react-bootstrap";
import FormInput from "../../form-input/FormInput";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useNavigate } from "react-router-dom";
import { login } from "../../../services/repartidor";

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

  const onSubmitFormSesion = async (values) => {
    try {
      const response = await login(values.username, values.password);
      if (!response.exito) {
        console.log("error");
        return;
      }
      const jsonResponse = JSON.stringify(response.respuesta);
      localStorage.setItem("repartidor", jsonResponse);
      navigate("/PedidosZona");
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <>
      <NavBar />
      <div className="w-4/5 flex flexs-col justify-center mx-auto">
        <Container>
          <div
            style={{
              display: "flex",
              justifyContent: "center",
              alignContent: "center",
              alignItems: "center",
            }}
          >
            <h1 style={{ margin: "7%" }} className="text-white">
              Login - Repartidor
            </h1>
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
    </>
  );
}

export default Login;
