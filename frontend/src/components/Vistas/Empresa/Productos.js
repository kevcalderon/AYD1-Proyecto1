import React, { useEffect, useMemo, useState } from "react";
import NavbarE from "../../Navbars/NavbarE";
import Container from "react-bootstrap/esm/Container";
import MaterialReactTable from "material-react-table";
import API_URL from "../../../app/constants";
import { Button } from "react-bootstrap";

function Productos() {
  const [productos, setProductos] = useState([]);
  // const urlDocs = process.env.REACT_APP_PUBLIC_DOCUMENTOS;

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
      // {
      //   accessorKey: "FOTOGRAFIA",
      //   header: "Imagen",
      //   id: "imagen",
      //   Cell: ({ row }) => (
      //     <div>
      //       <img
      //         src={`${urlDocs}${row.original.FOTOGRAFIA}`}
      //         alt="fgd"
      //         width="100px"
      //         height="100px"
      //         style={{ objectFit: "contain" }}
      //       />
      //     </div>
      //   ),
      // },
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
      </Container>
    </div>
  );
}

export default Productos;
