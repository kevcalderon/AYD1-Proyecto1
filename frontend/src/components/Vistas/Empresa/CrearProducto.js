import React from "react";
import NavbarE from "../../Navbars/NavbarE";
import { Button, Container, Form } from "react-bootstrap";
import { FormProvider, useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import FormInput from "../../form-input/FormInput";
import API_URL from "../../../app/constants";

function CrearProducto() {
  const validationSchema = z.object({
    nombre: z.string().min(1, { message: "Campo Obligatorio" }),
    descripcion: z.string().min(1, { message: "Campo Obligatorio" }),
    precio: z.string().min(1, { message: "Campo Obligatorio" }),
    stock: z.string().min(1, { message: "Campo Obligatorio" }),
    id_tipo_producto: z.string().min(1, { message: "Campo Obligatorio" }),

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

  const onSubmit = async (values) => {
    console.log(values);
    const empresa = JSON.parse(localStorage.getItem("empresa"));
    const formData = new FormData();
    formData.append("id_empresa", empresa.EMP_ID);
    formData.append("nombre", values.nombre);
    formData.append("descripcion", values.descripcion);
    formData.append("precio", values.precio);
    formData.append("stock", values.stock);
    formData.append("id_tipo_producto", values.id_tipo_producto);
    formData.append("documento", values.documento[0]);

    await fetch(`${API_URL}/crearProducto`, {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((res) => {
        console.log(res);
        if (res.exito == false) {
          // mostrarComponente(res.msg);
        } else {
          reset();
          // mostrarComponente(res.msg);
        }
      });

    reset();
  };

  return (
    <div>
      <NavbarE />

      <Container>
        <div style={{ display: "flex", margin: "2%" }}>
          <h1>Crear Producto</h1>
          <img
            src="https://cdn-icons-png.flaticon.com/512/2250/2250401.png"
            alt="crearPr"
            height="8%"
            width="8%"
          />
        </div>
        <div
          style={{
            backgroundColor: "#A8DADC",
            borderRadius: "20px",
            padding: "3%",
          }}
        >
          <FormProvider {...methods}>
            <Form onSubmit={handleSubmit(onSubmit)}>
              <FormInput
                placeholder="Nombre del producto"
                errors={errors}
                name="nombre"
                controlId="idNombre"
                type="text"
                register={register}
              />
              <FormInput
                placeholder="Descripción del producto"
                errors={errors}
                name="descripcion"
                controlId="idDescripcion"
                type="text"
                register={register}
              />
              <FormInput
                placeholder="Precio del producto"
                errors={errors}
                name="precio"
                controlId="idPrecio"
                type="text"
                register={register}
              />
              <FormInput
                placeholder="Stock del producto"
                errors={errors}
                name="stock"
                controlId="idStock"
                type="number"
                register={register}
              />
              <Form.Select name="tipoEmpresa" {...register("id_tipo_producto")}>
                <option>Escoge el tipo de producto</option>
                <option value="1">ENTRADAS</option>
                <option value="2">PLATOS FUERTES</option>
                <option value="3">POSTRES</option>
                <option value="4">BEBIDAS</option>
                <option value="5">PRODUCTOS DE ASEO</option>
                <option value="6">LIBRERIA</option>
                <option value="7">FERRETERIA</option>
                <option value="8">SNACKS</option>
                <option value="9">ELECTRONICOS</option>
                <option value="10">ARTICULOS DEPORTIVOS</option>
                <option value="11">VESTUARIO</option>
              </Form.Select>
              <br></br>
              <Form.Group controlId="formFile" className="mb-3">
                <Form.Label>Imagen del Producto</Form.Label>
                <Form.Control type="file" {...register("documento")} />
              </Form.Group>
              <Button type="submit" variant="primary">
                Registrar Producto
              </Button>
            </Form>
          </FormProvider>
        </div>
      </Container>
    </div>
  );
}

export default CrearProducto;
