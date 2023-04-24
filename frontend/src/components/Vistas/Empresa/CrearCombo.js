import React, { useEffect, useState } from "react";
import NavbarE from "../../Navbars/NavbarE";
import {
  Col,
  Container,
  Row,
  Form,
  Button,
  FloatingLabel,
} from "react-bootstrap";
import { FormProvider, useForm } from "react-hook-form";
import FormInput from "../../form-input/FormInput";
import API_URL from "../../../app/constants";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

function CrearCombo() {
  const [combosInfo, setCombosInfo] = useState([]);
  const [productoEmpresa, setProductoEmpresa] = useState([]);

  // VALIDACIONES DE FORMULARIO COMBO
  const validationSchemaCombo = z.object({
    nombre: z.string().min(1, { message: "Campo Obligatorio" }),
    descripcion: z.string().min(1, { message: "Campo Obligatorio" }),
    precio: z.string().min(1, { message: "Campo Obligatorio" }),
    nombre_archivo: z.any({ message: "Campo Obligatorio" }),
  });

  const methodsCombo = useForm({
    resolver: zodResolver(validationSchemaCombo),
  });

  const {
    reset: resetCombo,
    handleSubmit: handleSubmitCombo,
    register: registerCombo,
    formState: { errors },
  } = methodsCombo;

  const onSubmitCombo = async (values) => {
    console.log(values);

    const empresa = JSON.parse(localStorage.getItem("empresa"));
    const formData = new FormData();
    formData.append("nombre", values.nombre);
    formData.append("descripcion", values.descripcion);
    formData.append("precio", values.precio);
    formData.append("documento", values.nombre_archivo[0]);

    await fetch(`${API_URL}/crearCombo`, {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((res) => {
        console.log(res);
        if (res.exito == false) {
          // mostrarComponente(res.msg);
        } else {
          resetCombo();
          getUltimoCombo();
          // mostrarComponente(res.msg);
        }
      });

    // reset();
  };

  // VALIDACIONES DE COMBO ITEMS
  const validationSchemaComboItem = z.object({
    id_combo: z.string().min(1, { message: "Campo Obligatorio" }),
    id_producto: z.string().min(1, { message: "Campo Obligatorio" }),
    cantidad: z.string().min(1, { message: "Campo Obligatorio" }),
    observaciones: z.string().min(1, { message: "Campo Obligatorio" }),
  });

  const methodsComboItems = useForm({
    resolver: zodResolver(validationSchemaComboItem),
  });

  const {
    reset: resetComboItem,
    handleSubmit: handleSubmitComboItem,
    register: registerComboItem,
    formState: { errorsItem },
  } = methodsComboItems;

  const onSubmitComboItem = async (values) => {
    console.log(values);
    const empresa = JSON.parse(localStorage.getItem("empresa"));
    const formData = new FormData();
    formData.append("id_combo", values.id_combo);
    formData.append("id_producto", values.id_producto);
    formData.append("cantidad", values.cantidad);
    formData.append("observaciones", values.observaciones);

    await fetch(`${API_URL}/agregarProductoACombo`, {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((res) => {
        console.log(res);
        if (res.exito == false) {
          // mostrarComponente(res.msg);
        } else {
          resetComboItem();

          // mostrarComponente(res.msg);
        }
      });

    // reset();
  };

  const getProductos = async () => {
    const empresa = JSON.parse(localStorage.getItem("empresa"));

    await fetch(`${API_URL}/mostrarProductosEmpresa/${empresa.EMP_ID}`, {
      method: "GET",
    })
      .then((response) => response.json())
      .then((res) => {
        console.log(res);
        setProductoEmpresa(res);
      });
  };

  const getUltimoCombo = async () => {
    await fetch(`${API_URL}/VerUltimoComboInsertado`, {
      method: "GET",
    })
      .then((response) => response.json())
      .then((res) => {
        console.log(res);
        setCombosInfo(res.combo);
      });
  };

  useEffect(() => {
    getProductos();
  }, []);

  return (
    <div>
      <NavbarE />
      <Container>
        <div style={{ display: "flex", margin: "3%" }}>
          <h1>Crear Combo </h1>
          <img
            src="https://cdn-icons-png.flaticon.com/512/4221/4221407.png"
            alt="crearCombo"
            height="7%"
            width="7%"
          />
        </div>
        <Row>
          {/* CREAR COMBO */}
          <Col>
            <div
              style={{
                backgroundColor: "#A8DADC",
                borderRadius: "20px",
                padding: "3%",
              }}
            >
              <p>Información principal del combo</p>
              <FormProvider {...methodsCombo}>
                <Form onSubmit={handleSubmitCombo(onSubmitCombo)}>
                  <FormInput
                    placeholder="Nombre del combo"
                    errors={errors}
                    name="nombre"
                    controlId="idNombreCombo"
                    type="text"
                    register={registerCombo}
                  />
                  <FormInput
                    placeholder="Descripción del combo"
                    errors={errors}
                    name="descripcion"
                    controlId="idDescripcion"
                    type="text"
                    register={registerCombo}
                  />
                  <FormInput
                    placeholder="Precio del combo"
                    errors={errors}
                    name="precio"
                    controlId="idPrecio"
                    type="number"
                    register={registerCombo}
                  />
                  <Form.Group controlId="formFile" className="mb-3">
                    <Form.Label>Imagen del Producto</Form.Label>
                    <Form.Control
                      type="file"
                      {...registerCombo("nombre_archivo")}
                    />
                  </Form.Group>
                  <Button type="submit" variant="primary">
                    Registra combo
                  </Button>
                </Form>
              </FormProvider>
            </div>
          </Col>
          {/* CREAR ITEMS DEL COMBO */}
          <Col>
            <div
              style={{
                backgroundColor: "#A8DADC",
                borderRadius: "20px",
                padding: "3%",
              }}
            >
              <p>Agregar los productos al combo</p>
              <FormProvider {...methodsComboItems}>
                <Form onSubmit={handleSubmitComboItem(onSubmitComboItem)}>
                  <Form.Select
                    name="idCombo"
                    {...registerComboItem("id_combo")}
                  >
                    <option>Selecciona el ultimo combo</option>
                    {combosInfo.length === 0 ? (
                      <option></option>
                    ) : (
                      <option value={combosInfo.COM_ID}>
                        {combosInfo.NOMBRE}
                      </option>
                    )}
                  </Form.Select>
                  <br></br>
                  <Form.Select
                    name="id_producto"
                    {...registerComboItem("id_producto")}
                  >
                    <option>Escoge tu producto</option>
                    {productoEmpresa.map((producto, index) => {
                      return (
                        <option value={producto.PRO_ID} key={index}>
                          {producto.NOMBRE_PRODUCTO}
                        </option>
                      );
                    })}
                  </Form.Select>
                  <br></br>

                  <Form.Group className="mb-3">
                    <FloatingLabel
                      controlId="idCantidadProd"
                      label="Cantidad del producto"
                      className="mb-2"
                    >
                      <Form.Control
                        type="number"
                        placeholder="Cantidad del producto"
                        size="sm"
                        {...registerComboItem("cantidad")}
                      />
                    </FloatingLabel>
                  </Form.Group>
                  <Form.Group className="mb-3">
                    <FloatingLabel
                      controlId="idObservacionesProd"
                      label="Observaciones del producto"
                      className="mb-2"
                    >
                      <Form.Control
                        type="text"
                        placeholder="Observaciones del producto"
                        size="sm"
                        {...registerComboItem("observaciones")}
                      />
                    </FloatingLabel>
                  </Form.Group>
                  <Button type="submit" variant="warning">
                    Agregar el producto
                  </Button>
                </Form>
              </FormProvider>
            </div>
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default CrearCombo;
