import React, { useEffect, useMemo, useState } from "react";
import NavbarE from "../../Navbars/NavbarE";
import { Button, Container } from "react-bootstrap";
import API_URL from "../../../app/constants";
import MaterialReactTable from "material-react-table";

function VerCombos() {
  const [combos, setCombos] = useState([]);

  const verCombos = async () => {
    const empresa = JSON.parse(localStorage.getItem("empresa"));
    await fetch(`${API_URL}/mostrarCombosConProductos/${empresa.EMP_ID}`)
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setCombos(data.msg);
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

  const columns = useMemo(
    () => [
      {
        accessorKey: "DESCRIPCION",
        header: "Descripcion",
        id: "descripcion",
      },
      {
        accessorKey: "NOMBRE",
        header: "Nombre",
        id: "nombre",
      },
      {
        accessorKey: "PRECIO",
        header: "Precio",
        id: "precio",
      },
      // {
      //   accessorKey: "DETALLE_COMBO",
      //   header: "Detalle",
      //   id: "detalle",
      // },
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
              variant="danger"
              style={{ margin: "1.5%" }}
              // onClick={() => {
              //   eliminarProducto(row.original.PRO_ID);
              // }}
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

  useEffect(() => {
    verCombos();
  }, []);

  return (
    <div>
      <NavbarE />
      <br></br>
      <Container>
        <h1>C O M B O S </h1>
        <MaterialReactTable
          columns={columns}
          data={combos}
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

export default VerCombos;
