import React, { useEffect, useMemo, useState } from "react";
import NavbarE from '../../Navbars/NavbarE'
import { Button, Container } from "react-bootstrap";
import API_URL from "../../../app/constants";
import MaterialReactTable from "material-react-table";

function Reportes() {
  const [combos, setCombos] = useState([]);
  const [data, setData] = useState("");

  const top5 = async () => {
    const empresa = JSON.parse(localStorage.getItem("empresa"));
    await fetch(`${API_URL}/top5ProductosMasVendidos/${empresa.EMP_ID}`)
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setCombos(data.msg);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  useEffect(() => {
    const fetchData = async () => {
      const empresa = JSON.parse(localStorage.getItem("empresa"));
      const result = await fetch(`${API_URL}/obtenerNoPedidosYTotalVentas/${empresa.EMP_ID}`);
      const data = await result.json();
      setData(data.msg[0]);
      console.log(data.msg[0]);
    };

    fetchData();
  }, []);

  const columns = useMemo(
    () => [
      {
        accessorKey: "CANTIDAD_VENDIDOS",
        header: "Cantidad de vendidos",
        id: "cantidad_vendidos",
      },
      {
        accessorKey: "NOMBRE",
        header: "Nombre",
        id: "nombre",
      }
    ],
    []
  );

  useEffect(() => {
    top5();
  }, []);

  return (
    <div>
      <NavbarE />
      <br></br>
      <Container>
        <h1>R E P O R T E</h1>
        <h4>Información general</h4>
        <p><b>Cantidad de ordenes</b>: {data.CANTIDAD_ORDENES}</p>
        <p><b>Cantidad de ventas</b>: {data.CANTIDAD_VENTA}</p>

        <h4>Top 5</h4>
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

export default Reportes