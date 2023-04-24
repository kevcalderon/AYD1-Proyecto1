import { Backdrop, CircularProgress } from "@mui/material";
import React, { useMemo } from "react";
import { useQuery } from "react-query";
import {
  asignarPedido,
  fetchPedidosPendientes,
} from "../../../services/pedidos";
import NavBar from "../../Navbars/NavbarR";
import ShowError from "../../showError/ShowError";
import MaterialReactTable from "material-react-table";
import { fields } from "./PedidosZonaFields";

function PedidosZona() {
  const id_repartidor = localStorage.getItem("repartidor");
  const rawPedidosZona = useQuery(
    ["fetchPedidosPendientes", JSON.parse(id_repartidor)],
    fetchPedidosPendientes,
    { staleTime: 30000 }
  );

  const updatePedido = (id_orden) => {
    try {
      asignarPedido(JSON.parse(id_repartidor).USUARIO, id_orden);
    } catch (error) {
      console.log(error);
    }
  };

  const columns = useMemo(() => fields(updatePedido), []);
  const data = useMemo(() => rawPedidosZona.data, [rawPedidosZona.data]);

  if (rawPedidosZona.isLoading) {
    return (
      <Backdrop
        sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 1 }}
        open={rawPedidosZona.isLoading}
      >
        <CircularProgress color="inherit" />
      </Backdrop>
    );
  }

  if (rawPedidosZona.isError) {
    return (
      <ShowError
        title="Error"
        description="Estamos teniendo problemas al cargar esta pagina."
        message="Intenta recargar la pagina. Si el problema presiste comunicate con IT"
      />
    );
  }

  return (
    <div style={{ color: "white" }}>
      <NavBar />
      <div className="w-11/12 mx-auto mt-20">
        <MaterialReactTable
          columns={columns}
          data={data}
          enableColumnActions={false}
          enableColumnFilters={false}
          enablePagination={true}
          enableSorting={false}
          enableBottomToolbar={true}
          enableTopToolbar={true}
          muiTableBodyRowProps={{ hover: true }}
        />
      </div>
    </div>
  );
}

export default PedidosZona;
