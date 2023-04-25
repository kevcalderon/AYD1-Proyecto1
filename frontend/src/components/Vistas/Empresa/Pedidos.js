import React, { useEffect, useMemo, useState } from "react";
import NavbarE from "../../Navbars/NavbarE";
import API_URL from "../../../app/constants";
import { Badge, Button, Container } from "react-bootstrap";
import MaterialReactTable from "material-react-table";

function Pedidos() {
  const [pedidos, setPedidos] = useState([]);

  const verPedidosEmpresa = async () => {
    const empresa = JSON.parse(localStorage.getItem("empresa"));
    await fetch(`${API_URL}/mostrarOrdenes/${empresa.EMP_ID}`)
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        if (data.msg !== null) {
          setPedidos(data.msg);
        } else {
          setPedidos([]);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const aceptarRechazarProducto = async (
    idOrden,
    esCombo,
    idProducto,
    estado
  ) => {
    console.log(idOrden);
    console.log(esCombo);
    console.log(idProducto);
    console.log(estado);

    const formData = new FormData();
    formData.append("id_orden", idOrden);
    formData.append("estado", estado);
    if (esCombo === 1) {
      formData.append("id_combo", idProducto);
      formData.append("id_producto", "");
    } else {
      formData.append("id_combo", "");
      formData.append("id_producto", idProducto);
    }

    console.log(formData);
    await fetch(`${API_URL}/actualizarEstadoDetalleOrden`, {
      method: "PUT",
      // headers: { "Content-type": "application/json; charset=UTF-8" },
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        verPedidosEmpresa();
      })
      .catch((error) => {
        console.log(error);
      });
  };

  useEffect(() => {
    verPedidosEmpresa();
  }, []);

  const columns = useMemo(
    () => [
      {
        accessorKey: "NOMBRE_COMPLETO_REPARTIDOR",
        header: "Repartidor",
        id: "repartidor",
      },
      {
        accessorKey: "NOMBRE_COMPLETO_CLIENTE",
        header: "Cliente",
        id: "cliente",
      },
      {
        accessorKey: "LUGAR",
        header: "Lugar",
        id: "lugar",
      },
      {
        accessorKey: "FECHA",
        header: "Fecha",
        id: "fecha",
      },
      {
        accessorKey: "ESTADO",
        header: "Estado",
        id: "estado",
      },
      {
        accessorKey: "DETALLE_ORDEN",
        header: "Productos de orden para aceptar/rechazar",
        id: "productosAceptar",
        Cell: ({ row }) => (
          <div>
            {row.original.DETALLE_ORDEN.map((prod, index) => {
              return (
                <div style={{ padding: "3%" }} key={index}>
                  <li>{prod.NOMBRE_ARTICULO}</li>
                  <div style={{ display: "flex" }}>
                    {/* orden, combo, producto, estado */}
                    <Button
                      variant="success"
                      style={{ marginRight: "5px" }}
                      onClick={() => {
                        aceptarRechazarProducto(
                          row.original.ORD_ID,
                          prod.ES_COMBO,
                          prod.ID_ARTICULO,
                          "ACEPTADO"
                        );
                      }}
                    >
                      Aceptar
                    </Button>
                    <Button
                      variant="danger"
                      onClick={() => {
                        aceptarRechazarProducto(
                          row.original.ORD_ID,
                          prod.ES_COMBO,
                          prod.ID_ARTICULO,
                          "RECHAZADO"
                        );
                      }}
                    >
                      Rechazar
                    </Button>
                  </div>
                </div>
              );
            })}
          </div>
        ),
      },
    ],
    []
  );

  return (
    <div>
      <NavbarE />

      <br></br>
      <Container>
        <div style={{ display: "flex", margin: "2%" }}>
          <h1>P E D I D O S</h1>
          <img
            style={{ marginLeft: "20px" }}
            src="https://cdn-icons-png.flaticon.com/512/9405/9405321.png"
            alt="crearPr"
            height="8%"
            width="8%"
          />
        </div>
        <p>Acepta o rechaza los productos para preparar la orden.</p>
        {pedidos.length === 0 ? (
          <Badge bg="success" style={{ fontSize: "25px" }}>
            NO HAY PEDIDOS PARA TU EMPRESA! :D{" "}
          </Badge>
        ) : (
          <MaterialReactTable
            columns={columns}
            data={pedidos}
            enableColumnActions={false}
            enableColumnFilters={false}
            enablePagination={true}
            enableSorting={false}
            enableBottomToolbar={true}
            enableTopToolbar={true}
            muiTableBodyRowProps={{ hover: true }}
          />
        )}
      </Container>
    </div>
  );
}

export default Pedidos;
