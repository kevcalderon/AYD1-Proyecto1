import React, { useEffect, useMemo, useState } from "react";
import NavbarE from "../../Navbars/NavbarE";
import Container from "react-bootstrap/esm/Container";
import MaterialReactTable from "material-react-table";
import API_URL from "../../../app/constants";
import { Button, FloatingLabel, Form } from "react-bootstrap";
import Modal from "react-bootstrap/Modal";

function Productos() {
  const [productos, setProductos] = useState([]);
  const [show, setShow] = useState(false);
  const [productSelected, setProductoSelected] = useState({});

  const handleClose = () => setShow(false);
  const handleShow = (
    idProducto,
    descripcion,
    foto,
    nombre,
    precio,
    stock,
    idTipo
  ) => {
    let prod = {
      id_producto: idProducto,
      nombre: nombre,
      descripcion: descripcion,
      precio: precio,
      stock: stock,
      id_tipo_producto: idTipo,
      documento: foto,
    };
    setProductoSelected(prod);
    setShow(true);
  };

  const updateProducto = async () => {
    // console.log(productSelected);
    const formData = new FormData();
    formData.append("descripcion", productSelected.descripcion);
    formData.append("nombre", productSelected.nombre);
    formData.append("stock", String(productSelected.stock));
    formData.append("precio", String(productSelected.precio));
    formData.append(
      "id_tipo_producto",
      String(productSelected.id_tipo_producto)
    );
    formData.append("documento", productSelected.documento);

    await fetch(
      `${API_URL}/actualizarProducto/${productSelected.id_producto}`,
      {
        method: "PUT",
        body: formData,
      }
    )
      .then((response) => response.json())
      .then((res) => {
        console.log(res);
        verProductos();
        handleClose();
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const verProductos = async () => {
    const empresa = JSON.parse(localStorage.getItem("empresa"));
    await fetch(`${API_URL}/mostrarProductosEmpresa/${empresa.EMP_ID}`)
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setProductos(data);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const obtenerImagen = async (valueImage) => {
    await fetch(`${API_URL}/descargarArchivo/${valueImage}`, {
      method: "GET",
      headers: { "Content-type": "multipart/form-data; charset=UTF-8" },
    }).then((response) => {
      response.blob().then((blob) => {
        let url = window.URL.createObjectURL(blob);
        let a = document.createElement("a");
        a.href = url;
        a.download = valueImage;
        a.click();
      });
    });
  };

  const eliminarProducto = async (idProducto) => {
    await fetch(`${API_URL}/eliminarProducto/${idProducto}`, {
      method: "DELETE",
      headers: { "Content-type": "application/json; charset=UTF-8" },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        verProductos();
      })
      .catch((error) => {
        console.log(error);
      });
  };

  useEffect(() => {
    verProductos();
  }, []);

  const columns = useMemo(
    () => [
      {
        accessorKey: "NOMBRE_PRODUCTO",
        header: "Nombre",
        id: "nombre",
      },
      {
        accessorKey: "NOMBRE_TIPO_PRODUCTO",
        header: "Tipo",
        id: "tipo",
      },
      {
        accessorKey: "PRECIO",
        header: "Precio",
        id: "precio",
      },
      {
        accessorKey: "STOCK",
        header: "Stock",
        id: "stock",
      },
      {
        accessorKey: "FOTOGRAFIA",
        header: "Imagen",
        id: "imagen",
        Cell: ({ row }) => (
          <div>
            <Button
              variant="link"
              onClick={() => {
                obtenerImagen(row.original.FOTOGRAFIA);
              }}
            >
              Descargar imagen
            </Button>
          </div>
        ),
      },
      {
        Header: "Acciones",
        accessor: "acciones",
        id: "actions",
        Cell: ({ row }) => (
          <div>
            <Button
              variant="info"
              style={{ margin: "1.5%" }}
              onClick={() => {
                // añadirFav(row.original.PEL_ID);
                handleShow(
                  row.original.PRO_ID,
                  row.original.DESCRIPCION,
                  row.original.FOTOGRAFIA,
                  row.original.NOMBRE_PRODUCTO,
                  row.original.PRECIO,
                  row.original.STOCK,
                  row.original.T_PRO_ID
                );
              }}
            >
              <div
                style={{
                  display: "flex",
                  justifyContent: "center",
                  alignContent: "center",
                  alignItems: "center",
                }}
              >
                <p style={{ margin: "5%" }}>Actualizar</p>
                <img
                  src="https://cdn-icons-png.flaticon.com/512/5278/5278646.png"
                  width="28px"
                  height="8px"
                  alt="fav"
                />
              </div>
            </Button>
            <Button
              variant="danger"
              style={{ margin: "1.5%" }}
              onClick={() => {
                eliminarProducto(row.original.PRO_ID);
              }}
            >
              <div
                style={{
                  display: "flex",
                  justifyContent: "center",
                  alignContent: "center",
                  alignItems: "center",
                }}
              >
                <p style={{ margin: "5%" }}>Eliminar</p>
                <img
                  src="https://cdn-icons-png.flaticon.com/512/5676/5676146.png"
                  width="28px"
                  height="8px"
                  alt="fav"
                />
              </div>
            </Button>
          </div>
        ),
      },
    ],
    []
  );

  return (
    <div style={{ color: "white" }}>
      <NavbarE />
      <br></br>
      <Container>
        <h1>Productos </h1>
        <MaterialReactTable
          columns={columns}
          data={productos}
          enableColumnActions={false}
          enableColumnFilters={false}
          enablePagination={true}
          enableSorting={false}
          enableBottomToolbar={true}
          enableTopToolbar={true}
          muiTableBodyRowProps={{ hover: true }}
        />
        <Modal show={show} onHide={handleClose}>
          <Modal.Header closeButton>
            <Modal.Title>Actualizar Producto</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <Form>
              <Form.Group className="mb-3">
                <FloatingLabel
                  controlId="idNombreUpdate"
                  label="Nombre de producto"
                  className="mb-2"
                >
                  <Form.Control
                    type="text"
                    placeholder="Nombre de producto"
                    size="sm"
                    value={productSelected?.nombre}
                    onChange={(e) =>
                      setProductoSelected({
                        ...productSelected,
                        nombre: e.target.value,
                      })
                    }
                  />
                </FloatingLabel>
              </Form.Group>
              <Form.Group className="mb-3">
                <FloatingLabel
                  controlId="idDescripcionUpdate"
                  label="Descripcion de producto"
                  className="mb-2"
                >
                  <Form.Control
                    type="text"
                    placeholder="Descripcion de producto"
                    size="sm"
                    value={productSelected?.descripcion}
                    onChange={(e) =>
                      setProductoSelected({
                        ...productSelected,
                        descripcion: e.target.value,
                      })
                    }
                  />
                </FloatingLabel>
              </Form.Group>
              <Form.Group className="mb-3">
                <FloatingLabel
                  controlId="idPrecioUpdate"
                  label="Precio de producto"
                  className="mb-2"
                >
                  <Form.Control
                    type="text"
                    placeholder="Precio de producto"
                    size="sm"
                    value={productSelected?.precio}
                    onChange={(e) =>
                      setProductoSelected({
                        ...productSelected,
                        precio: e.target.value,
                      })
                    }
                  />
                </FloatingLabel>
              </Form.Group>
              <Form.Group className="mb-3">
                <FloatingLabel
                  controlId="idStockUpdate"
                  label="Stock de producto"
                  className="mb-2"
                >
                  <Form.Control
                    type="number"
                    placeholder="Stock de producto"
                    size="sm"
                    value={productSelected?.stock}
                    onChange={(e) =>
                      setProductoSelected({
                        ...productSelected,
                        stock: e.target.value,
                      })
                    }
                  />
                </FloatingLabel>
              </Form.Group>
              <Form.Select
                name="tipoEmpresa"
                value={productSelected.id_tipo_producto}
                onChange={(e) =>
                  setProductoSelected({
                    ...productSelected,
                    id_tipo_producto: e.target.value,
                  })
                }
              >
                <option>Escoge el tipo de producto</option>
                <option
                  value="1"
                  selected={productSelected.id_tipo_producto === 1}
                >
                  ENTRADAS
                </option>
                <option
                  value="2"
                  selected={productSelected.id_tipo_producto === 2}
                >
                  PLATOS FUERTES
                </option>
                <option
                  value="3"
                  selected={productSelected.id_tipo_producto === 3}
                >
                  POSTRES
                </option>
                <option
                  value="4"
                  selected={productSelected.id_tipo_producto === 4}
                >
                  BEBIDAS
                </option>
                <option
                  value="5"
                  selected={productSelected.id_tipo_producto === 5}
                >
                  PRODUCTOS DE ASEO
                </option>
                <option
                  value="6"
                  selected={productSelected.id_tipo_producto === 6}
                >
                  LIBRERIA
                </option>
                <option
                  value="7"
                  selected={productSelected.id_tipo_producto === 7}
                >
                  FERRETERIA
                </option>
                <option
                  value="8"
                  selected={productSelected.id_tipo_producto === 8}
                >
                  SNACKS
                </option>
                <option
                  value="9"
                  selected={productSelected.id_tipo_producto === 9}
                >
                  ELECTRONICOS
                </option>
                <option
                  value="10"
                  selected={productSelected.id_tipo_producto === 10}
                >
                  ARTICULOS DEPORTIVOS
                </option>
                <option
                  value="11"
                  selected={productSelected.id_tipo_producto === 11}
                >
                  VESTUARIO
                </option>
              </Form.Select>
              <br></br>
              <Form.Group
                controlId="formFile"
                className="mb-3"
                onChange={(e) =>
                  setProductoSelected({
                    ...productSelected,
                    documento: e.target.files[0],
                  })
                }
              >
                <Form.Label>Imagen del Producto</Form.Label>
                <Form.Control type="file" />
              </Form.Group>
              <Modal.Footer>
                <Button variant="secondary" onClick={handleClose}>
                  Close
                </Button>
                <Button
                  variant="primary"
                  type="button"
                  onClick={updateProducto}
                >
                  Save Changes
                </Button>
              </Modal.Footer>
            </Form>
          </Modal.Body>
        </Modal>
      </Container>
    </div>
  );
}

export default Productos;
