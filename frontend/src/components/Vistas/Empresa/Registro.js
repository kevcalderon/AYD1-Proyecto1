import React, { useEffect, useState } from "react";
import NavBar from "../../Navbars/NavbarU";
import Container from "react-bootstrap/Container";
import { FormProvider, useForm } from "react-hook-form";
import { Button, Form } from "react-bootstrap";
import FormInput from "../../form-input/FormInput";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useNavigate } from "react-router-dom";
import API_URL from "../../../app/constants";
import AutoCompleteForm from "../../autocomplete/Autocomplete";

function Registro() {
  const navigate = useNavigate();
  const [tiposEmpresa, setTiposEmpresa] = useState([]);
  const [departamentos, setDepartamentos] = useState([]);
  const [municipios, setMunicipios] = useState([]);
  const [mostrarAlert, setMostrarAlert] = useState(false);
  const [msg, setMsg] = useState("");
  const validationSchema = z.object({
    nombre: z.string().min(1, { message: "Campo Obligatorio" }),
    descripcion: z.string().min(1, { message: "Campo Obligatorio" }),
    correo: z.string().email({ message: "Direccion de email no valida." }),
    telefono: z.string().min(5, { message: "Ingresa un numero valido" }),
    usuario: z.string().min(1, { message: "Campo Obligatorio" }),
    contrasenia: z.string().min(1, { message: "Campo Obligatorio" }),
    nit: z.string().min(1, { message: "Campo Obligatorio" }),
    id_tipo_empresa: z.string().min(1, { message: "Campo Obligatorio" }),
    lugar: z.string().min(1, { message: "Campo Obligatorio" }),
    id_municipio: z.string().min(1, { message: "Campo Obligatorio" }),
    documento: z.any(),
  });

  const methods = useForm({
    resolver: zodResolver(validationSchema),
  });

  const {
    reset,
    handleSubmit,
    register,
    formState: { errors },
  } = methods;

  function mostrarComponente(msgAlert) {
    setMostrarAlert(true);
    setMsg(msgAlert);
    setTimeout(() => setMostrarAlert(false), 5000);
  }

  const getTiposEmpresa = async () => {
    await fetch(`${API_URL}/mostrarTiposEmpresa`)
      .then((response) => response.json())
      .then((res) => {
        setTiposEmpresa(res);
      });
  };

  const getDepartamentos = async () => {
    await fetch(`${API_URL}/mostrarDepartamentos`)
      .then((response) => response.json())
      .then((res) => {
        // console.log(res);
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

  const onSubmitFormSesion = async (values) => {
    console.log(values.documento[0]);
    const formData = new FormData();
    formData.append("nombre", values.nombre);
    formData.append("descripcion", values.descripcion);
    formData.append("correo", values.correo);
    formData.append("telefono", values.telefono);
    formData.append("usuario", values.usuario);
    formData.append("contrasenia", values.contrasenia);
    formData.append("nit", values.nit);
    formData.append("id_tipo_empresa", values.id_tipo_empresa);
    formData.append("lugar", values.lugar);
    formData.append("id_municipio", values.id_municipio);
    formData.append("documento", values.documento[0]);

    await fetch(`${API_URL}/crearEmpresa`, {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((res) => {
        // console.log(res);
        if (res.exito == false) {
          mostrarComponente(res.msg);
        } else {
          reset();
          mostrarComponente(res.msg);
        }
      });
  };

  useEffect(() => {
    getTiposEmpresa();
    getDepartamentos();
  }, []);

  return (
    <div>
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
          <h1 style={{ margin: "7%" }}>Registro - Empresa</h1>
          <img
            src="https://cdn-icons-png.flaticon.com/512/3200/3200751.png"
            width="150px"
            height="150px"
            alt="loginImg"
          />
        </div>

        <div>
          <FormProvider {...methods}>
            <Form onSubmit={handleSubmit(onSubmitFormSesion)}>
              <FormInput
                placeholder="Nombre de la empresa"
                errors={errors}
                name="nombre"
                controlId="idNombre"
                type="text"
                register={register}
              />
              <FormInput
                placeholder="Descripcion"
                errors={errors}
                name="descripcion"
                controlId="idDescripcion"
                type="text"
                register={register}
              />
              <FormInput
                placeholder="Correo"
                errors={errors}
                name="correo"
                controlId="idCorreo"
                type="text"
                register={register}
              />
              <FormInput
                placeholder="Teléfono"
                errors={errors}
                name="telefono"
                controlId="idTeléfono"
                type="text"
                register={register}
              />
              <FormInput
                placeholder="Usuario"
                errors={errors}
                name="usuario"
                controlId="idUsuario"
                type="text"
                register={register}
              />
              <FormInput
                placeholder="Password"
                errors={errors}
                name="contrasenia"
                controlId="idContrasenia"
                type="password"
                register={register}
              />
              <FormInput
                placeholder="Nit de la empresa"
                errors={errors}
                name="nit"
                controlId="idNit"
                type="text"
                register={register}
              />
              <Form.Select name="tipoEmpresa" {...register("id_tipo_empresa")}>
                <option>Escoge el tipo de empresa</option>
                {tiposEmpresa.map((tipo) => {
                  return (
                    <option key={tipo.T_EMP_ID} value={tipo.T_EMP_ID}>
                      {tipo.NOMBRE}
                    </option>
                  );
                })}
              </Form.Select>
              <br></br>
              <Form.Select
                name="departamento"
                onChange={(e) => {
                  handleSelect(e.target.value);
                }}
              >
                <option>Escoge el departamento</option>

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
              <br></br>
              <Form.Select name="municipio" {...register("id_municipio")}>
                <option>Escoge el municipio</option>
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
              <br></br>
              <FormInput
                placeholder="Lugar de la empresa"
                errors={errors}
                name="lugar"
                controlId="idLugar"
                type="text"
                register={register}
              />
              <Form.Group controlId="formFile" className="mb-3">
                <Form.Label>Documento</Form.Label>
                <Form.Control type="file" {...register("documento")} />
              </Form.Group>
              {mostrarAlert && (
                <div
                  className="alert alert-dismissible alert-danger"
                  style={{ margin: "3%" }}
                >
                  <strong>{msg}</strong>
                </div>
              )}
              <Button variant="warning" type="submit">
                Registrar
              </Button>
            </Form>
          </FormProvider>
        </div>
      </Container>
    </div>
  );
}

export default Registro;
